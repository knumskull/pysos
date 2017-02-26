# -*- coding: utf-8 -*-
"""
Created on Dec 27, 2013

@author: wallace
"""


class Host:
    """
    This class will represent hosts in an environment
    """

    # CHANGED: In this branch I'm moving from the vds_static table to the vds view - a single view with information from both status and dynamic tables
    __uuid = ""
    __name = ""
    __host_dc_uuid = ""
    __host_dc_name = "unknown"
    __ip_addr = ""
    __host_name = ""
    __host_type = ""
    __spm_status = ""
    __releaseVer = "unknown"
    __vdsm_ver = ""
    __host_os = ""
    __kvm_ver = ""
    __spice_ver = ""
    __kernel_ver = ""
    __selinux = "Unknown"  # Setting to unknown by default since the variable is set in the rhevm.py file. if the file can't be found or opened, unknown is returned

    schema31 = {
        "uuid": 0,
        "name": 1,
        "host_dc_uuid": 6,
        "ip_addr": 2,
        "host_name": 4,
        "host_type": 8,
        "vdsm_ver": 39,
        "host_os": 27,
        "kvm_ver": 28,
        "spice_ver": 29,
        "kernel_ver": 30
    }
    schema32 = {
        "uuid": 0,
        "name": 1,
        "host_dc_uuid": 6,
        "ip_addr": 2,
        "host_name": 4,
        "host_type": 8,
        "vdsm_ver": 37,
        "host_os": 25,
        "kvm_ver": 26,
        "spice_ver": 27,
        "kernel_ver": 28
    }
    schema33 = {
        "uuid": 0,
        "name": 1,
        "host_dc_uuid": 6,
        "ip_addr": 2,
        "host_name": 4,
        "host_type": 8,
        "vdsm_ver": 38,
        "host_os": 26,
        "kvm_ver": 27,
        "spice_ver": 28,
        "kernel_ver": 29
    }
    schema34 = {
        "uuid": 0,
        "name": 1,
        "host_dc_uuid": 6,
        "ip_addr": 2,
        "host_name": 4,
        "host_type": 8,
        "vdsm_ver": 36,
        "host_os": 25,
        "kvm_ver": 26,
        "spice_ver": 27,
        "kernel_ver": 28
    }
    schema35 = {
        "uuid": 0,
        "name": 1,
        "host_dc_uuid": 6,
        "ip_addr": 2,
        "host_name": 4,
        "host_type": 8,
        "vdsm_ver": 35,
        "host_os": 24,
        "kvm_ver": 25,
        "spice_ver": 26,
        "kernel_ver": 27
    }
    schema36 = {
        "uuid": 0,
        "name": 1,
        "host_dc_uuid": 5,
        "ip_addr": 2,
        "host_name": 3,
        "host_type": 7,
        "vdsm_ver": 35,
        "host_os": 24,
        "kvm_ver": 25,
        "spice_ver": 26,
        "kernel_ver": 27
    }

    def __init__(self, csvList, dbVersion):
        """
        This constructor assumes it is being passed a comma separated list consisting of all elements in a line from the dat file
        """
        details = csvList

        if len(details) > 2:
            self.current_schema = "3.3"   # arbitrary, just to set a default
            if dbVersion == "3.1":
                self.current_schema = self.schema31
            elif dbVersion == "3.2":
                self.current_schema = self.schema32
            elif dbVersion == "3.3":
                self.current_schema = self.schema33
            elif dbVersion == "3.4":
                self.current_schema = self.schema34
            elif dbVersion == "3.5":
                self.current_schema = self.schema35
            elif dbVersion == "3.6":
                self.current_schema = self.schema36

            self.uuid = details[self.current_schema['uuid']]
            self.name = details[self.current_schema['name']]
            self.host_dc_uuid = details[self.current_schema['host_dc_uuid']]
            self.ip_addr = details[self.current_schema['ip_addr']]
            self.host_name = details[self.current_schema['host_name']]
            self.type = details[self.current_schema['host_type']]
            # determine host type from input
            if self.type == "0":
                self.type = "RHEL"
            elif self.type == "2":
                self.type = "RHEV-H"
            self.host_dc_name = 'unknown'

    @property
    def get_spm_status(self):
        return self.__spm_status

    @property
    def spm_status(self):
        return self.__spm_status

    @spm_status.setter
    def spm_status(self, value):
        self.__spm_status = value

    @property
    def host_dc_name(self):
        return self.__host_dc_name

    @host_dc_name.setter
    def host_dc_name(self, value):
        self.__host_dc_name = value

    @property
    def spm(self):
        return self.__spm_status

    @property
    def release_ver(self):
        return self.__releaseVer

    @spm.setter
    def spm(self, value):
        self.__spm_status = value

    @release_ver.setter
    def release_ver(self, value):
        self.__releaseVer = value

    @property
    def selinux(self):
        return self.__selinux

    @selinux.setter
    def selinux(self, status):
        self.__selinux = status

    @property
    def type(self):
        return self.__host_type

    @type.setter
    def type(self, value):
        self.__host_type = value

    @property
    def uuid(self):
        return self.__uuid

    @property
    def name(self):
        return self.__name

    @property
    def host_dc_uuid(self):
        return self.__host_dc_uuid

    @property
    def ip_addr(self):
        return self.__ip_addr

    @property
    def host_name(self):
        return self.__host_name

    @uuid.setter
    def uuid(self, value):
        self.__uuid = value

    @name.setter
    def name(self, value):
        self.__name = value

    @host_dc_uuid.setter
    def host_dc_uuid(self, value):
        self.__host_dc_uuid = value

    @ip_addr.setter
    def ip_addr(self, value):
        self.__ip_addr = value

    @host_name.setter
    def host_name(self, value):
        self.__host_name = value

    @property
    def vdsm_ver(self):
        return self.__vdsm_ver

    @vdsm_ver.setter
    def vdsm_ver(self, value):
        self.__vdsm_ver = value

    @property
    def host_os(self):
        return self.__host_os

    @property
    def kvm_ver(self):
        return self.__kvm_ver

    @property
    def spice_ver(self):
        return self.__spice_ver

    @property
    def kernel_ver(self):
        return self.__kernel_ver

    def __repr__(self):
        print("Host name: " + self.name)
        print("VDSM Ver: " + self.vdsm_ver)

    def updateHostDynamic(self, dynamic_list):

        self.vdsm_ver = dynamic_list[self.current_schema['vdsm_ver']]
        if 'vdsm' not in self.vdsm_ver:
            self.vdsm_ver = "error"
        else:
            self.vdsm_ver = self.vdsm_ver.split("vdsm-")[1].rstrip('\n')
        self.__host_os = dynamic_list[self.current_schema['host_os']].replace(' ', '')
        self.__kvm_ver = dynamic_list[self.current_schema['kvm_ver']].replace(' ', '')
        self.__spice_ver = dynamic_list[self.current_schema['spice_ver']].replace(' ', '')
        self.__kernel_ver = dynamic_list[self.current_schema['kernel_ver']].replace(' ', '')
