# -*- coding: utf-8 -*-
import sys
import os
from .color import Color as c


class Object(object):
    pass


class lspci():

    """ Capture and optionally display hardware device information """

    def __init__(self, target):
        self.target = target
        self.lspciInfo = self._getLspciInfo()
        self.pprint = c()

    def _getLspciInfo(self):
        if os.path.isfile(self.target + 'sos_commands/hardware/lspci'):
            lspciInfo = []
            with open(self.target +
                      'sos_commands/hardware/lspci', 'r') as lfile:
                for line in lfile:
                    if 'lspci -nvv:' in line:
                        break
                    try:
                        pciaddr = line[0:line.find('.') - 1].strip()
                        newDev = True
                        if len(lspciInfo) > 0:
                            for dev in lspciInfo:
                                if dev.pciaddr == pciaddr:
                                    dev.count += 1
                                    newDev = False
                                    break
                        if newDev:
                            dev = Object()
                            dev.pciaddr = pciaddr
                            dev.devtype = line[line.find(pciaddr):
                                               line.find(': ') + 1].strip(
                                pciaddr).strip()
                            dev.name = line[line.find(': ') + 2:
                                            len(line)].strip('\n')
                            if 'Ethernet' in dev.devtype:
                                dev.devtype = 'Ethernet'
                            elif 'VGA' in dev.devtype:
                                dev.devtype = 'VGA'
                            elif 'SCSI' in dev.devtype:
                                dev.devtype = 'SCSI'
                            elif 'Fibre Channel' in dev.devtype:
                                dev.devtype = 'Fibre HBA'
                            dev.count = 1
                            lspciInfo.append(dev)
                    except:
                        pass

            return lspciInfo
        else:
            return False

    def displayLspciInfo(self, chkType):
        """ Display hardware devices for the given type of device """
        for dev in self.lspciInfo:
            if chkType in dev.devtype:
                if dev.count > 1:
                    self.pprint.bheader(
                        '\t\t {:10} : '.format(dev.devtype),
                        '[{} ports] '.format(dev.count),
                        dev.name
                    )
                else:
                    self.pprint.bheader(
                        '\t\t {:10} : '.format(dev.devtype),
                        '{}'.format(dev.name)
                    )

    def displayAllLspciInfo(self):
        """ Helper for displaying the most common device types """
        self.pprint.bsection('LSPCI')
        if self.lspciInfo:
            self.pprint.bheader('\t Physical Devices')
            # Not really *all*, just all we're interesting in
            self.displayLspciInfo('Ethernet')
            self.displayLspciInfo('Network')
            self.displayLspciInfo('IPMI')
            self.displayLspciInfo('VGA')
            self.displayLspciInfo('SCSI')
            self.displayLspciInfo('Fibre')
        else:
            self.pprint.bred('\t LSPCI Information Not Found')

if __name__ == '__main__':
    target = sys.argv[1]
    test = lspci(target)
    test.displayAllLspciInfo()
