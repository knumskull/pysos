# -*- coding: utf-8 -*-
import os
import sys
import tarfile
import pysosutils
from color import Color as c
from rhevlcbridge import Database, Cluster, Table, Host, StorageDomain


class Object(object):
    pass


class rhevm():

    def __init__(self, target, db=False):
        self.target = target
        self.db = db
        self.rhevm = self.getRhevmInfo()
        self.pprint = c()

    def getRhevmVer(self):
        return pysosutils.getRpmVer(self.target, 'rhevm')

    def getReportsVer(self):
        return pysosutils.getRpmVer(self.target, 'rhevm-reports')

    def getDwhVer(self):
        return pysosutils.getRpmVer(self.target, 'rhevm-dwh')

    def getRhevmInfo(self):
        rhevm = Object()
        rhevm.ver = self.getRhevmVer()
        rhevm.reports = self.getReportsVer()
        rhevm.dwh = self.getDwhVer()
        return rhevm

    def _rhevmSimpleVer(self):
        rhevm = self.getRhevmVer()
        if "3.0" in rhevm:
            simpleVer = "3.0"
        elif "3.1" in rhevm:
            simpleVer = "3.1"
        elif "3.2" in rhevm:
            simpleVer = "3.2"
        elif "3.3" in rhevm:
            simpleVer = "3.3"
        elif "3.4" in rhevm:
            simpleVer = "3.4"
        elif "3.5" in rhevm:
            simpleVer = "3.5"
        elif "3.6" in rhevm:
            simpleVer = "3.6"
        else:
            simpleVer = "Could not be found"
        return simpleVer

    def checkForDb(self):
        fullPath = os.path.abspath(self.target)
        lcRoot = os.path.join(os.path.dirname(fullPath), 'log-collector-data')

        rhevm_hostname = self.__get_rhevm_hostname()
        try:
            db_file = pysosutils.dir_entries(lcRoot, True, 'sos_pgdump.tar')[0]
        except IndexError:
            # extract the postgresql-sosreport-* file
            sosreport = pysosutils.dir_entries(lcRoot, False, 'postgresql-sosreport*', '.xz')[0]
            with tarfile.open(sosreport) as f:
                f.extractall(path=lcRoot)
            try:
                db_file = pysosutils.dir_entries(lcRoot, True, 'sos_pgdump.tar')[0]
            except IndexError:
                return False

        return db_file

    def parseDb(self):
        db = self.checkForDb()
        simpleVer = self._rhevmSimpleVer()
        if db:
            if (simpleVer == "3.1" or simpleVer == "3.2" or
                    simpleVer == "3.3" or simpleVer == "3.4" or
                    simpleVer == "3.5" or simpleVer == "3.6"):
                self.displayDbEval(db, simpleVer)
            elif simpleVer == "3.0":
                self.pprint.warn("\t 3.0 parsing not implemented")
            else:
                self.pprint.warn(
                    "\t Database version needed for proper analysis"
                )
        else:
            self.pprint.warn("Database not found")

    def parseEngineLog(self):
        logFile = open(os.path.join(self.target, 'var/log/ovirt-engine/engine.log'), 'r')
        # Find most recent error line
        lines = logFile.readlines()
        errorLines = []
        for line in lines:
            if "ERROR" in line:

                errorLines.append(line)
        print('')

        for x in range(1, 4):
            try:
                lastLine = len(errorLines) - x
                errorLine = errorLines[lastLine]
                errorProperties = errorLine.split(" ")
                '''
                0 - Date
                1 - Time
                3 - Command run
                7+ - Message
                '''
                self.pprint.bheader("\t Time Stamp: ",
                                    errorProperties[
                                        0] + " " + errorProperties[1]
                                    )
                self.pprint.bheader("\t Command: ",
                                    errorProperties[3].lstrip("[").rstrip("]")
                                    )
                # Trying to hack this since messages varies in length
                # basing on last capital letter. deal with it
                errMessParts = errorProperties[7:]
                errorMessage = ""
                for p in errMessParts:
                    # print p
                    for c in p:
                        if c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                            # print errMessParts.index(p)
                            index = errMessParts.index(p)
                            errorMessage = ' '.join(errMessParts[index:]
                                                    ).replace("\n", "")
                            # print errorMessage

                self.pprint.bheader("\t Message: ", errorMessage)
                singleOccurance = True
                occurances = 0
                for line in lines:
                    if ' '.join(errorProperties[7:]) in line:
                        occurances += 1
                if occurances > 1:
                    singleOccurance = False

                if singleOccurance:
                    self.pprint.bheader(
                        "\t Only occurance of this error: ",
                        "Yes"
                    )
                else:
                    self.pprint.bheader(
                        "\t Only occurance of this error: ",
                        "No. Errors appear " + str(occurances),
                        " times in engine.log starting at ",
                        ' '.join(errorLines[0].split(" ")[0:2])
                    )
                print("")
            except:
                pass
        logFile.close()

    def displayRhevmInfo(self):
        self.pprint.bblue('\t\t This is a RHEV Manager')
        print('')
        self.pprint.bheader('\t RHEV-M Version : ', self.rhevm.ver)
        self.pprint.bheader('\t RHEV-M Reports : ', self.rhevm.reports)
        self.pprint.bheader('\t RHEV-M DWH     : ', self.rhevm.dwh)
        print('')
        dbPresent = self.checkForDb()
        if dbPresent:
            self.pprint.blue('\t Database found. Can parse.')
        else:
            self.pprint.red("\t Database not found. Can't parse.")
        print('')
        print('\t Most recent errors in engine.log : ')
        self.parseEngineLog()
        if self.db:
            self.parseDb()

    def getMasterDbObj(self):
        dbTar = os.path.join(self.checkForDb())
        simpleVer = self._rhevmSimpleVer()
        masterDB = Database(dbTar, simpleVer)
        return masterDB

    def getDcList(self):
        masterDB = self.getMasterDbObj()
        return masterDB.data_centers

    def getClusterList(self):
        masterDB = self.getMasterDbObj()
        return masterDB.clusters

    def displayRhevDcInfo(self):
        masterDB = self.getMasterDbObj()
        # create DC list
        dcList = self.getDcList()
        print("")
        self.pprint.bsection("RHEV Database Information")
        print("")
        self.pprint.bgreen('\n\t[Data Centers Managed By RHEV-M]')
        dc_table = Table(dcList, "name", "uuid", "compat")
        dc_table.display()

    def displayRhevStorageInfo(self):
        masterDB = self.getMasterDbObj()
        self.pprint.breen('\n\t[Storage Domains In All Data Centers]')
        sd_list = masterDB.storage_domains
        sd_list.sort(key=lambda x: x.storage_type)
        sd_table = Table(sd_list, "name", "uuid", "storage_type", "master")
        sd_table.display()

    def displayRhevClusterInfo(self):
        masterDB = self.getMasterDbObj()
        self.pprint.bgreen('\n\t[Clusters In All Data Centers]')
        clusterList = self.getClusterList()
        clusterList.sort(key=lambda x: x.dc_uuid)
        cluster_table = Table(clusterList, "name", "uuid", "compat_ver",
                              "cpu_type", "dc_uuid")
        cluster_table.display()

    def displayRhevHyperInfo(self):
        dbDir = self.checkForDb()
        dcList = self.getDcList()
        clusterList = self.getClusterList()
        masterDB = self.getMasterDbObj()
        host_list = masterDB.hosts
        hostDirs = []
        hostNameLen = 5
        # look for all files in the parent of the passed 'dbDir'
        # and if it is a dir then attempts to parse
        rootDir = os.path.dirname(dbDir)
        for data_center in os.listdir(rootDir):
            if os.path.isdir(os.path.join(rootDir, data_center)):
                hostDirs.append(data_center)
        # creating list of hosts without sosreports
        missFingHostNames = []
        host_list.sort(key=lambda x: x.name)
        for host in host_list:
            for data_center in dcList:
                if host.uuid == data_center.spm_uuid:
                    host.spm_status = True
                else:
                    host.spm_status = False
            for cluster in clusterList:
                if cluster.uuid == host.host_dc_uuid:
                    for data_center in dcList:
                        if cluster.dc_uuid == data_center.uuid:
                            host.host_dc_name = data_center.name
            # try and find release version
            hostDirName = host.name.split(".")
            for dir in hostDirs:
                names = dir.split("-")
                # found a bug where all sosreport folders were lowercase
                # but hostDirName was uppercase
                if names[0] == hostDirName[0].lower():
                    # this is a stupid hack, using '..' in the path name
                    # stop being lazy and find a better alternative
                    releaseFile = open(os.path.join(dbDir, "/../", dir, "/etc/redhat-release"))
                    releaseVer = releaseFile.readlines()
                    if "Hypervisor" in releaseVer[0]:
                        host_release = releaseVer[0].split("(")[1]
                        # strip the newline character at the end of line
                        host_release = host_release.replace("\n", "")
                        host_release = host_release.rstrip(")")
                        host.set_release_ver(host_release)
                    else:
                        host_release = releaseVer[0].split()[6]
                        host.set_release_ver(host_release)
                    host.set_selinux(pysosutils.getSeLinux(os.path.join(dbDir, "/../", dir), ['current']))
                else:
                    pass
        self.pprint.bgreen('\n\t[Hypervisors In All Data Centers]')
        host_table = Table(host_list, "name", "uuid", "host_dc_name",
                           "type", "spm", "selinux")
        host_table.display()

        self.pprint.bgreen('\n\t[RPM Versions on All Hypervisors]')
        host_ver_table = Table(host_list, "name", "host_os", "vdsm_ver",
                               "kvm_ver", "spice_ver", "kernel_ver")
        host_ver_table.display()

    def displayDbEval(self, db, simpleVer):
        self.displayRhevDcInfo()
        self.displayRhevClusterInfo()
        self.displayRhevStorageInfo()
        self.displayRhevHyperInfo()

    def __get_rhevm_hostname(self):
        return pysosutils.fileToString(os.path.join(self.target, 'hostname'))

if __name__ == '__main__':
    target = sys.argv[1]
    test = rhevm(target, True)
    test.displayRhevmInfo()
