# -*- coding: utf-8 -*-
"""
Created on Dec 27, 2013

@author: wallace
"""


class DataCenter:
    """ This class will represent hosts in an environment """

    __uuid = ""
    __name = ""
    __compat = ""
    __spm_uuid = ""

    # since each db version changes a little bit, we need to define the index of each field in the dat file
    schema31 = {
        "uuid": 0,
        "name": 1,
        "compat": 8,
        "spm_uuid": 7
    }
    schema32 = {
        "uuid": 0,
        "name": 1,
        "compat": 8,
        "spm_uuid": 7
    }
    schema33 = {
        "uuid": 0,
        "name": 1,
        "compat": 8,
        "spm_uuid": 7
    }
    schema34 = {
        "uuid": 0,
        "name": 1,
        "compat": 8,
        "spm_uuid": 7
    }
    schema35 = {
        "uuid": 0,
        "name": 1,
        "compat": 8,
        "spm_uuid": 7
    }
    schema36 = {
        "uuid": 0,
        "name": 1,
        "compat": 8,
        "spm_uuid": 7
    }

    def __init__(self, csvList, dbVersion):
        """ This constructor assumes it is being passed a comma separated list consisting of all elements in a line from the dat file

        :param csvList:
        :param dbVersion:
        """
        details = csvList

        current_schema = "3.3"   # arbitrary, just to set a default
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
            self.__uuid = details[current_schema['uuid']]
            self.__name = details[current_schema['name']]
            self.__compat = details[current_schema['compat']]
            self.__spm_uuid = details[current_schema['spm_uuid']]

    @property
    def uuid(self):
        return self.__uuid

    @property
    def name(self):
        return self.__name

    @property
    def compat(self):
        return self.__compat

    @property
    def spm_uuid(self):
        return self.__spm_uuid

    @uuid.setter
    def uuid(self, value):
        self.__uuid = value

    @name.setter
    def name(self, value):
        self.__name = value

    @compat.setter
    def compat(self, value):
        self.__compat = value

    @spm_uuid.setter
    def spm_uuid(self, value):
        self.__spm_uuid = value
