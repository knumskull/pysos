# -*- coding: utf-8 -*-
import glob
import sys
import os
import re
from collections import OrderedDict


def fileToString(filepath):
    """
    For single line files, read the file in and return
    contents as a string.
    """
    try:
        with open(filepath, 'r') as f:
            return f.readline().strip('\n')
    except IOError:
        return '%s not found' % filepath


def getCmdLine(target):
    """ Get the booted kernel cmdline options """
    return fileToString(os.path.join(target, 'proc/cmdline'))


def getRelease(target):
    """ Get the OS release """
    return fileToString(os.path.join(target, 'etc/redhat-release'))


def getKernelVersion(target):
    """ Get the booted kernel version """
    uname = fileToString(os.path.join(target, 'sos_commands/kernel/uname_-a'))
    return uname.split()[2]


def getRpm(target, rpm, boolean=False):
    """
    Get details on a given rpm.

    Boolean option can be used to see if rpm is installed or not.
    """
    rpms = []
    if os.path.isfile(os.path.join(target, 'installed-rpms')):
        with open(os.path.join(target, 'installed-rpms'), 'r') as rfile:
            for line in rfile:
                if line.startswith(rpm):
                    index = line.find('.')
                    thisRpm = line[0:index - 2]
                    if thisRpm == rpm:
                        if boolean:
                            return True
                        else:
                            rpms.append(line.split()[0])
    if len(rpms) == 0:
        if boolean:
            return False
        else:
            rpms.append("Not Installed")
    return rpms


def getRpmVer(target, rpm):
    """ Get _just_ the version of a given RPM """
    ver = getRpm(target, rpm)[0]
    if 'Not Installed' in ver:
        return ver
    else:
        formatVer = ver.strip(rpm).strip('x86_64').strip(
            'noarch').strip('-').strip('.')
        return formatVer


def checkRpm(target, rpm):
    """
    This function will check pysosweb DB for any known issues
    for a given RPM and version.
    """
    return "Not yet implemented"


def getSysctl(target, sysctl):
    """ Get the setting for a given sysctl """
    sysctls = {}
    if os.path.isfile(os.path.join(target, 'sos_commands/kernel/sysctl_-a')):
        with open(os.path.join(target, 'sos_commands/kernel/sysctl_-a'),
                  'r') as sysfile:
            for line in sysfile:
                if sysctl in line:
                    name = line.split()[0]
                    value = line.split()[2]
                    sysctls[name] = value
    else:
        sysctls = "No sysctl_-a file to parse"
    return sysctls


def getChkConfig(target, service):
    """
    Check the current service configuration from chkconfig.

    TO DO: expand to systemd.
    """
    if os.path.isfile(os.path.join(target, 'chkconfig')):
        with open(os.path.join(target, 'chkconfig'), 'r') as cfile:
            for line in cfile:
                if service in line:
                    serviceStatus = line.lstrip(service).rstrip(
                        '\n').lstrip()
                    return serviceStatus
        return "Service not found in chkconfig"
    else:
        return "No chkconfig file found"


def getSeLinux(target):
    """ Get the current and configured SELinux setting """
    selStatus = {}
    if os.path.isfile(os.path.join(target, 'sos_commands/selinux/sestatus_-b')):
        with open(os.path.join(target, 'sos_commands/selinux/sestatus_-b'),
                  'r') as sfile:
            for i, line in enumerate(sfile):
                index = line.find(':')
                if line.startswith('SELinux status'):
                    selStatus['status'] = line[index + 1:
                                               len(line)].strip()
                    if selStatus['status'] == 'disabled':
                        selStatus['current'] = 'disabled'
                        selStatus['config'] = 'disabled'
                        break
                elif line.startswith('Current'):
                    selStatus['current'] = line[index + 1:
                                                len(line)].strip()
                elif line.startswith('Mode'):
                    selStatus['config'] = line[index + 1:
                                               len(line)].strip()
                elif i > 6:
                    break
    else:
        selStatus['current'] = 'Not Found'
        selStatus['config'] = 'Not Found'
    return selStatus


def getTaintCodes(target):
    """
    Get the current taint state of the kernel and return a
    description of the code along with the numerical code.
    """
    t = OrderedDict()
    t['536870912'] = "Technology Preview code is loaded"
    t['268435456'] = "Hardware is unsupported"
    t['134217728'] = "Taint by Zombie"
    t['4096'] = "Out-of-tree module has been loaded"
    t['2048'] = "Working around severe firmware bug"
    t['1024'] = "Modules from drivers/staging are loaded"
    t['512'] = "Kernel warning occurred"
    t['256'] = "ACPI table overridden"
    t['128'] = "Kernel has oopsed before"
    t['64'] = "Unsigned kernel modules"
    t['32'] = "System has hit bad_page"
    t['16'] = "System experienced a machine check exception"
    t['8'] = "User forced a module unload"
    t['4'] = "SMP with CPUs not designed for SMP"
    t['2'] = "Module has been forcibly loaded"
    t['1'] = "Proprietary module has been loaded"
    t['0'] = "Not tainted. Hooray!"

    with open(os.path.join(target, 'proc/sys/kernel/tainted'), 'r') as tfile:
        check = tfile.read().splitlines()
        check = check[0]
        # if check in t:
        #    return t[check]
        # else:
        check = int(check)
        taintCodes = []
        for key in t:
            if int(check) - int(key) > int('-1'):
                taintCodes.append(('%4s - ' % (key) + t[key]).strip('\n'))
                check = int(check) - int(key)
                if check == 0:
                    return taintCodes
            else:
                pass
        # we should only hit this if we have an undefined taint code
        taintCodes.append("Undefined taint code: %s") % str(check)
        return taintCodes


def parseOutputSection(fname, section):
    """
    Given a filename (fname) and a section header, parse the file
    and then return all content between the section header and
    a new line, signifying the end of the section.
    """
    if os.path.isfile(fname):
        with open(fname, 'r') as pfile:
            handle_regex = re.compile('^%s\s' % section)
            newline = re.compile('^$')
            lines = pfile.readlines()
            for x in range(0, len(lines)):
                line = lines[x]
                if handle_regex.findall(line):
                    # Found header for section
                    sectionInfo = {}
                    sectionInfo['info'] = []
                    while True:
                        try:
                            line = lines[x + 1]
                    # repeat until we hit newline
                            if not newline.findall(line):
                                sectionInfo['info'].append(line.strip(
                                ).strip('\t'))
                                x += 1
                            else:
                                break
                        except:
                            break
                    info = {}
                    for item in sectionInfo['info']:
                        try:
                            key = item.split(':')[0]
                            value = item.split(':')[1]
                            info[key] = value.strip()
                        except:
                            pass
        try:
            return info
        except UnboundLocalError:
            return False
    else:
        return False


def dir_entries(dir_name, recursive=False, filter_exp=None, *extensions):
    """
    Return a list of file names found in directory 'dir_name'
    If 'recursive' is True, subdirectories in 'dir_name' will be scanned recursively.
    Found filters will be matched against the given filter_exp, e.g. '*motor*'.
    Set 'filter_exp' to None if you want no filtering.
    Additional arguments, if provided, are file extensions to be matched. Only files
    matching the filter and extensions (if given) are added to the list.
    If neither a filter nor extensions are provided, all files found in the directory
    are returned.

    Example usage: fileList = dir_entries(r'/tmp', False, None, '.txt', '.py')
    Only files with '.txt' and '.py' extensions will be added to the list.
    Example usage: fileList = dirEntries(r'/tmp', True)
    All files (also those in the subdirectories of '/tmp/) will be added
    to the list.
    """
    file_list = []
    if os.access(dir_name, os.F_OK & os.R_OK):
        if filter_exp:
            filtered = glob.glob(os.path.join(dir_name, filter_exp))
        else:
            filtered = None
        for entry in os.listdir(dir_name):
            entry = os.path.join(dir_name, entry)
            if os.path.isdir(entry):
                if recursive:
                    file_list.extend(dir_entries(entry, recursive, filter_exp, *extensions))
            else:
                if filter_exp:
                    if not entry in filtered:
                        continue
                if extensions:
                    if not os.path.splitext(entry)[1] in extensions:
                        continue
                file_list.append(entry)
    return file_list
