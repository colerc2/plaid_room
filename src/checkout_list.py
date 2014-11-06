#!/usr/bin/python

class CheckoutList():
    def __init__(self):
        self.current_list = []
        self.number_in_list = 0
    
    def add_row(self, row):
        self.current_list.append(row)

    def get_size(self):
        return len(self.current_list)
