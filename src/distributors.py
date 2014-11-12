#!/usr/bin/python

import csv

class Distributors():
    def __init__(self):
        self.dist_file_name = '/Users/bccole1989/Documents/plaid_room_records/plaid_room/distributors.csv'
        distributor_file = open(self.dist_file_name)
        before_split = distributor_file.readline().rstrip('\n')
        distributor_file.close()
        self.distributor_list = before_split.split(',')

    def get_distributors(self):
        return self.distributor_list

    def add_distributor(self, addition):
        addition = addition.strip()
        if len(addition) >= 2:
            if addition not in self.distributor_list:
                with open(self.dist_file_name, "a") as distributor_file:
                    distributor_file.write(',%s' % addition)
                    self.distributor_list.append(addition)
                
                
