#!/usr/bin/python

import csv

class MiscDistributors():
    def __init__(self, misc_distributor_file):
        self.dist_file_name = misc_distributor_file
        misc_distributor_file = open(self.dist_file_name)
        before_split = misc_distributor_file.readline().rstrip('\n')
        misc_distributor_file.close()
        self.misc_distributor_list = before_split.split(',')

    def get_misc_distributors(self):
        return self.misc_distributor_list

    def add_misc_distributor(self, addition):
        addition = addition.strip()
        if len(addition) >= 2:
            if addition not in self.misc_distributor_list:
                with open(self.dist_file_name, "a") as misc_distributor_file:
                    misc_distributor_file.write(',%s' % addition)
                    self.misc_distributor_list.append(addition)
                
                
