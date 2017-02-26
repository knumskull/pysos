# -*- coding: utf-8 -*-
import sys
import os
from .color import Color as c


class Object(object):
    pass


class procInfo:

    """ Get and optionally display information from ps output """

    def __init__(self, target):
        self.target = target
        self.psInfo = self.parseProcFile()
        self.pprint = c()

    def parseProcFile(self):
        """
        Parse through a ps output file and return the contents
        as list vaues
        """
        if os.path.isfile(
                os.path.join(self.target, 'sos_commands/process/ps_auxwww')):
            psInfo = []
            stats = ['user', 'pid', 'cpu', 'mem', 'vsz', 'rss',
                     'tty', 'stat', 'start', 'time']
            with open(os.path.join(self.target, 'sos_commands/process/ps_auxwww'), 'r') as psfile:
                next(psfile)
                for line in psfile:
                    proc = Object()
                    line = line.split()
                    try:
                        for x, stat in enumerate(stats):
                            setattr(proc, stat, line[x])
                        proc.command = ' '.join(line[10:-1])
                        proc.shortcmd = proc.command.split()[0]
                        proc.vszmb = int(proc.vsz) / 1024
                        proc.rssmb = int(proc.rss) / 1024
                        psInfo.append(proc)
                    except:
                        pass
            return psInfo
        else:
            return False

    def getNumProcs(self):
        """ Get the number of processes running """
        return len(self.psInfo)

    def getUserReport(self):
        """ Get a report on CPU and RSS usage by user """
        usage = []
        for proc in self.psInfo:
            newProc = True
            if len(usage) > 0:
                for p in usage:
                    if p.user == proc.user:
                        p.cpu += float(proc.cpu)
                        p.mem += float(proc.mem)
                        p.rss += int(proc.rss)
                        newProc = False
                        break
            if newProc:
                proc.cpu = float(proc.cpu)
                proc.mem = float(proc.mem)
                proc.rss = int(proc.rss)
                usage.append(proc)
        userReport = sorted(usage, reverse=True,
                            key=lambda x: x.cpu)
        return userReport

    def _formatTopReport(self, psInfo, reportNum=5):
        report = []
        for i in range(0, int(reportNum)):
            proc = self.psInfo[i]
            cmd = ''
            for i in range(10, 13):
                try:
                    cmd = str(proc.command).strip('\n')

                except:
                    pass
            report.append(proc)
        return report

    def getTopMem(self, reportNum=5):
        """ Get report on top memory consuming processes """
        topMemReport = self._formatTopReport(self.psInfo.sort(
            reverse=True, key=lambda x: float(x.rss)))
        return topMemReport

    def getTopCpu(self, reportNum=5):
        """ Get report on top CPU consuming processes """
        topCpuReport = self._formatTopReport(self.psInfo.sort(
            reverse=True, key=lambda x: float(x.cpu)))
        return topCpuReport

    def getDefunctProcs(self):
        """ Get report of all defunct processess """
        badProcs = []
        for proc in self.psInfo:
            if ('<defunct>' in proc.command or
                    'D' in proc.stat or
                    'Ds' in proc.stat):
                badProcs.append(proc)
        return badProcs

    def getAllPsInfo(self):
        proc = Object()
        proc.psinfo = self.psInfo
        proc.numprocs = self.getNumProcs()
        proc.topuserreport = self.getUserReport()
        proc.topmemreport = self.getTopMem()
        proc.topcpureport = self.getTopCpu()
        proc.defunct = self.getDefunctProcs()
        return proc

    def displayReport(self, report):

        self.pprint.bblue(
            '\t {:^6}\t{:^6}\t{:^5} {:^5}  {:^7}  {:^7}  {:^4} {:^4}  {:^5}{:^8}  {:<8}'.format(
                'USER', 'PID', '%CPU', '%MEM', 'VSZ-MB', 'RSS-MB',
                'TTY', 'STAT', 'START', 'TIME', 'COMMAND'
            )
        )

        for proc in report:
            print('\t{:^8} {:<6}\t{:^5} {:^5}  {:<7.0f}  {:<7.0f}  {:^5} {:4} {:^6} {:<9}{}'.format(
                proc.user, proc.pid,
                proc.cpu, proc.mem, proc.vszmb, proc.rssmb, proc.tty,
                proc.stat, proc.start, proc.time,
                proc.command[0:45].strip()))

    def displayTopReport(self):
        """ Display report from getUserReport() """
        numProcs = self.getNumProcs()
        usageReport = self.getUserReport()
        self.pprint.white('\tTotal Processes : ', str(numProcs), '\n')

        self.pprint.white('\tTop Users of CPU and Memory : ')
        self.pprint.bblue('\t{:10}  {:6}  {:6}  {:8}'.format(
            'USER', '%CPU', '%MEM', 'RSS'
        )
        )

        for i in range(0, 4):
            proc = usageReport[i]
            print('\t {:<10}  {:^6.2f}  {:^6.2f}  {:>3.2f} GB'.format(
                proc.user, proc.cpu, proc.mem,
                int(proc.rss) / 1048576))
        print('')

    def displayCpuReport(self):
        """ Display report from getTopCpu() """
        cpuReport = self.getTopCpu()
        self.pprint.white('\tTop CPU Consuming Processes : ')
        self.displayReport(cpuReport)
        print('')

    def displayMemReport(self):
        """ Display report from getTopMem() """
        memReport = self.getTopMem()
        self.pprint.white('\tTop Memory Consuming Processes : ')
        self.displayReport(memReport)
        print('')

    def displayDefunctReport(self):
        """ Display report from getDefunctProcs() """
        defunctReport = self.getDefunctProcs()
        if defunctReport:
            self.pprint.bred(
                '\tUninterruptable Sleep and Defunct Processes : '
            )
            defunctReport = self._formatTopReport(defunctReport,
                                                  reportNum=len(defunctReport))
            self.displayReport(defunctReport)
            print('')

    def displayPsInfo(self):
        """ display ps information for top consumers, CPU, memory and
        defunct process, if any """
        self.pprint.bsection('PS')
        if self.psInfo:
            self.displayTopReport()
            self.displayDefunctReport()
            self.displayCpuReport()
            self.displayMemReport()
        else:
            self.pprint.BRED('No PS information found')


if __name__ == '__main__':
    target = sys.argv[1]
    test = procInfo(target)
    test.displayPsInfo()
