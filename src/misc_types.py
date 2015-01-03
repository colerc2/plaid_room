#!/usr/bin/python

import csv

class MiscTypes():
    def __init__(self, misc_types_file):
        self.misc_types_file_name = misc_types_file
        misc_types_file = open(self.misc_types_file_name)
        before_split = misc_types_file.readline().rstrip('\n')
        misc_types_file.close()
        self.misc_types_list = before_split.split(',')

    def get_misc_types(self):
        return self.misc_types_list

    def add_misc_type(self, addition):
        addition = addition.strip()
        if len(addition) >= 2:
            if addition not in self.misc_types_list:
                with open(self.misc_types_file_name, "a") as misc_types_file:
                    misc_types_file.write(',%s' % addition)
                    self.misc_types_list.append(addition)
                
                
