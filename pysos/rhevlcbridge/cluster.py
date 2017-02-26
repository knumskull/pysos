# -*- coding: utf-8 -*-
"""
Created on Dec 27, 2013

@author: wallace
"""


class Cluster:
    """ This class will represent hosts in an environment """

    __uuid = ""
    __name = ""
    __cpu_type = ""
    __dc_uuid = ""
    __compat_ver = ""

    schema31 = {
        "uuid": 0,
        "name": 1,
        "cpu_type": 3,
        "dc_uuid": 11,
        "compat_ver": 13,
    }
    schema32 = {
        "uuid": 0,
        "name": 1,
        "cpu_type": 3,
        "dc_uuid": 11,
        "compat_ver": 12,
    }
    schema33 = {
        "uuid": 0,
        "name": 1,
        "cpu_type": 3,
        "dc_uuid": 6,
        "compat_ver": 8,
    }
    schema34 = {
        "uuid": 0,
        "name": 1,
        "cpu_type": 3,
        "dc_uuid": 6,
        "compat_ver": 8,
    }
    schema35 = {
        "uuid": 0,
        "name": 1,
        "cpu_type": 3,
        "dc_uuid": 6,
        "compat_ver": 8,
    }
    schema36 = {
        "uuid": 0,
        "name": 1,
        "cpu_type": 3,
        "dc_uuid": 6,
        "compat_ver": 8,
    }

    def __init__(self, csvList, dbVersion):
        """
        This constructor assumes it is being passed a comma separated list consisting of all elements in a line from the dat file

        :param csvList:
        :param dbVersion:
        """

        details = csvList

        current_schema = "3.3"  # arbitrary, just to set a default
        if dbVersion == "3.1":
            current_schema = self.schema31
        elif dbVersion == "3.2":
            current_schema = self.schema32
        elif dbVersion == "3.3":
            current_schema = self.schema33
        elif dbVersion == "3.4":
            current_schema = self.schema34
        elif dbVersion == "3.5":
            current_schema = self.schema35
        elif dbVersion == "3.6":
            current_schema = self.schema36

        if len(details) > 2:
            self.uuid = details[current_schema['uuid']]
            self.name = details[current_schema['name']]
            self.cpu_type = details[current_schema['cpu_type']]
            self.dc_uuid = details[current_schema['dc_uuid']]
            if len(self.dc_uuid) != 36:
                self.dc_uuid = details[6]  # 3.3 and 3.4 moved this column to the 6th position instead of 11
            self.compat_ver = details[current_schema['compat_ver']]
            #print self.dc_uuid
            #print len(self.dc_uuid)
            if len(self.dc_uuid) != 36:
                self.dc_uuid = details[10]
            #print "We made a cluster!"

    @property
    def dc_uuid(self):
        return self.__dc_uuid

    @dc_uuid.setter
    def dc_uuid(self, value):
        self.__dc_uuid = value

    @property
    def compat_ver(self):
        return self.__compat_ver

    @compat_ver.setter
    def compat_ver(self, value):
        self.__compat_ver = value

    @property
    def get_uuid(self):
        return self.__uuid

    @property
    def get_name(self):
        return self.__name

    @property
    def get_cpu_type(self):
        return self.__cpu_type

    @property
    def uuid(self):
        return self.__uuid

    @uuid.setter
    def uuid(self, value):
        self.__uuid = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def cpu_type(self):
        return self.__cpu_type

    @cpu_type.setter
    def cpu_type(self, value):
        self.__cpu_type = value
