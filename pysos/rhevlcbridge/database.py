# -*- coding: utf-8 -*-
'''
Created on Dec 27, 2013

@author: wallace
'''
import tarfile
import os

import pysosutils
from .host import Host  # Surely there is a better way to do this
from .storagedomain import StorageDomain
from .datacenter import DataCenter
from .cluster import Cluster
from .task import Task


class Database:
    """
    This class should be created by passing the sos_pgdump.tar file to it

    It will serve the purpose of pulling information from the tar file without the need to upload to a dbviewer
    """

    ''' Start declaring variables for the class '''
    dbDir = ""
    tarFile = ""
    dat_files = []  # this is a list for all the wanted dat files
    __data_centers = []
    __storage_domains = []
    __hosts = []
    __clusters = []
    __tasks = []
    dbVersion = ""

    def __init__(self, database_file, database_version):
        """ Constructor """
        self.dbVersion = database_version
        self.dbDir = os.path.dirname(database_file)
        self.unpack(database_file)

        # Now that we're unpacked, move on to gathering information
        self.__data_centers = self.gatherDataCenters(database_version)
        self.__storage_domains = self.gatherStorageDomains(database_version)
        self.__hosts = self.gatherHosts(database_version)
        self.__clusters = self.gatherClusters(database_version)
        self.__tasks = self.gatherTasks(database_version)

    @property
    def clusters(self):
        return self.__clusters

    @clusters.setter
    def clusters(self, value):
        self.__clusters = value

    @clusters.deleter
    def clusters(self):
        del self.__clusters

    @property
    def data_centers(self):
        return self.__data_centers

    @property
    def storage_domains(self):
        return self.__storage_domains

    @property
    def hosts(self):
        return self.__hosts

    @property
    def tasks(self):
        return self.__tasks

    def unpack(self, db_tar_file):
        # Start with extraction
        tarfile.open(db_tar_file).extractall(self.dbDir)

        # create list of dat files
        self.dat_files = ["data_center_dat",
                          "storage_domain_dat",
                          "host_dat",
                          "cluster_dat",
                          "async_tasks_dat",
                          "host_dynamic_dat"]

        try:
            restore_sql = pysosutils.dir_entries(self.dbDir, False, 'restore.sql')[0]
            self.dat_files[0] = self.dat_files[0] + "," + self.findDat(" storage_pool ", restore_sql)
            self.dat_files[1] = self.dat_files[1] + "," + self.findDat(" storage_domain_static ", restore_sql)
            self.dat_files[2] = self.dat_files[2] + "," + self.findDat(" vds_static ", restore_sql)
            self.dat_files[3] = self.dat_files[3] + "," + self.findDat(" vds_groups ", restore_sql)
            self.dat_files[4] = self.dat_files[4] + "," + self.findDat(" async_tasks ", restore_sql)
            self.dat_files[5] = self.dat_files[5] + "," + self.findDat(" vds_dynamic ", restore_sql)

        except IndexError:
            print("Failed to parse 'restore.sql' file")

    @staticmethod
    def findDat(table, restore_file):
        """ Subroutine to find the .dat file name in restore.sql """

        with open(restore_file, "r") as fd:
            for line in fd.readlines():
                if line.find(table) != -1:
                    if line.find("dat") != -1:
                        datInd = line.find("PATH")
                        datFileName = line[datInd + 7:datInd + 15]
                        if datFileName.endswith("dat"):
                            return datFileName


    def gatherDataCenters(self, dbVersion):
        """ This method returns a list of comma-separated details of the Data Center """
        dc_list = []
        dat_file = os.path.join(self.dbDir, self.dat_files[0].split(",")[1])
        with open(dat_file, "r") as fd:
            for line in fd.readlines():
                if len(line.split("\t")) > 1:
                    dc_list.append(DataCenter(line.split("\t"), dbVersion))

        return dc_list

    def gatherStorageDomains(self, dbVersion):
        """ This method returns a list of comma-separated details of the Storage Domains

        :param dbVersion:
        :return:
        """
        sd_list = []
        dat_file = os.path.join(self.dbDir, self.dat_files[1].split(",")[1])
        with open(dat_file, "r") as fd:
            for line in fd.readlines():
                if len(line.split("\t")) > 1:
                    sd_list.append(StorageDomain(line.split("\t"), dbVersion))

        return sd_list

    def gatherClusters(self, dbVersion):
        """ This method returns a list of comma separated details for clusters

        :param dbVersion:
        :return:
        """
        cl_list = []
        dat_file = os.path.join(self.dbDir, self.dat_files[3].split(",")[1])

        with open(dat_file, "r") as fd:
            for line in fd.readlines():
                if len(line.split("\t")) > 1:
                    cl_list.append(Cluster(line.split("\t"), dbVersion))

        return cl_list

    def gatherHosts(self, dbVersion):
        """ This method returns a list of comma-separated details of the Data Center

        :param dbVersion:
        :return:
        """
        host_list = []
        static_dat_file = os.path.join(self.dbDir, self.dat_files[2].split(",")[1])
        dynamic_dat_file = os.path.join(self.dbDir, self.dat_files[5].split(",")[1])

        with open(static_dat_file, "r") as fd:
            for line in fd.readlines():
                if len(line.split("\t")) > 1:
                    host_list.append(Host(line.split("\t"), dbVersion))

        with open(dynamic_dat_file, "r") as fd:
            # fill in vds_dynamic information
            for host in host_list:
                h_uuid = host.uuid
                for line in fd.readlines():  # cycle through all lines in vds_dynamic file
                    if h_uuid in line:  # if this line correlates to the current host
                        host.updateHostDynamic(line.split("\t"))  # send line to Host method as a list

        return host_list

    def gatherTasks(self, dbVersion):
        """

        :param dbVersion:
        :return:
        """
        task_list = []
        dat_file = os.path.join(self.dbDir, self.dat_files[4].split(",")[1])

        with open(dat_file, "r") as fd:
            for line in fd.readlines():
                if len(line.split("\t")) > 1:
                    task_list.append(Task(line.split("\t"), dbVersion))

        return task_list
