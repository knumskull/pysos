# -*- coding: utf-8 -*-
"""
Created on Dec 27, 2013

@author: wallace
"""


class StorageDomain:
    """
    This class will represent hosts in an environment
    """

    __uuid = ""
    __name = ""
    __storage_type = ""
    __master = False

    schema31 = {
        "uuid": 0,
        "name": 2,
        "storage_type": 4,
        "master": 3,
    }
    schema32 = {
        "uuid": 0,
        "name": 2,
        "storage_type": 4,
        "master": 3,
    }
    schema33 = {
        "uuid": 0,
        "name": 2,
        "storage_type": 4,
        "master": 3,
    }
    schema34 = {
        "uuid": 0,
        "name": 2,
        "storage_type": 4,
        "master": 3,
    }
    schema35 = {
        "uuid": 0,
        "name": 2,
        "storage_type": 4,
        "master": 3,
    }
    schema36 = {
        "uuid": 0,
        "name": 2,
        "storage_type": 4,
        "master": 3,
    }

    def __init__(self, csvList, dbVersion):
        """
        This constructor assumes it is being passed a comma separated list consisting of all elements in a line from the dat file

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
            self.uuid = details[current_schema['uuid']]
            self.name = details[current_schema['name']]
            # determine storage medium
            self.storage_type = details[current_schema['storage_type']]
            if self.storage_type == "0":
                self.storage_type = "Local?"
            elif self.storage_type == "1":
                self.storage_type = "NFS"
            elif self.storage_type == "2":
                self.storage_type = "FCP"
            elif self.storage_type == "3":
                self.storage_type = "iSCSI"
            elif self.storage_type == "7":
                self.storage_type = "Gluster"
            self.master = False
            if details[current_schema['master']] == "0":
                self.master = True

    @property
    def uuid(self):
        return self.__uuid

    @property
    def name(self):
        return self.__name

    @property
    def storage_type(self):
        return self.__storage_type

    @property
    def master(self):
        return self.__master

    @uuid.setter
    def uuid(self, value):
        self.__uuid = value

    @name.setter
    def name(self, value):
        self.__name = value

    @storage_type.setter
    def storage_type(self, value):
        self.__storage_type = value

    @master.setter
    def master(self, value):
        self.__master = value
