#!/usr/bin/python

import sys
import openpyxl
from config_stuff import *
from openpyxl.styles import NamedStyle, Font, Border, Side
import locale
import re
import collections


class ColemineBooks():
    def __init__(self, yr, q):
        self.wb = openpyxl.load_workbook(COLEMINE_BOOKS_FILE)
        self.data_input = self.wb.get_sheet_by_name(name = 'Data Input')
        self.projects = self.wb.get_sheet_by_name(name = 'Project & Royalties')
        locale.setlocale (locale.LC_ALL, '' )
        self.non_decimal = re.compile(r'[^\d.]+')
        self.year = yr
        self.quarter = q 
        
    def get_projects(self):
        #get all projects
        p = self.projects['C']

        projects_set = set()
        for index, row in enumerate(p):
            if index == 0:
                continue
            try:
                projects_set.add(row.value.lower())
            except Exception as e:
                projects_set.add(row.value)
                print e
        sorted_projects = sorted(projects_set)
        #for row in sorted_projects:
        #    print row
        return sorted_projects

    def get_royalty_codes(self):
        #get all royalty codes
        r = self.projects['D']

        royalty_set = set()
        for row in r:
            try:
                royalty_set.add(row.value.lower())
            except Exception as e:
                royalty_set.add(row.value)
                #print e
        sorted_royalty = sorted(royalty_set)
        return sorted_royalty
        
        #print data_input
        #sheet_ranges = data_input['range names']
        #print sheet_ranges

    def get_payees(self):
        #p = self.projects['A']
        #codes
        payees_set = set()

        for index, row in enumerate(self.projects):
            if index == 0:
                continue
            if len(str(row[3].value)) < 2 or row[3].value is None:
                #this is a project summary, not a payee
                print 'This is a summary, not a payee: %s - %s' % (str(row[0].value),str(row[1].value))
                continue
            try:
                payees_set.add(row[0].value.lower().strip())
            except Exception as e:
                print 'couldnt add payee to list: %s - %s' % (str(row[0].value), e)
        sorted_payees = sorted(payees_set)
        print '--------------------------'
        for row in sorted_payees:
            print row
        print '--------------------------'
        return sorted_payees
        
    def get_sales_categories(self):
        #get all categories
        categories = self.data_input['E']

        sales_categories = set()
        for row in categories:
            try:
                sales_categories.add(row.value.lower())
            except Exception as e:
                print 'tried to add a none type to categories: %s' % e    
        print sales_categories

    def get_project_status(self):
        project_codes = self.get_projects()
        project_status = {} #new dict
        for pro in project_codes:
            project_status[str(pro)] = 0.0
        for row in self.data_input:
            this_adjustment_project = row[2].value
            try:
                this_adjustment_project = this_adjustment_project.lower()
            except Exception as e:
                placeholder = 0
            print '--%s--' % this_adjustment_project
            found = False
            if str(this_adjustment_project) in project_status:
                project_status[str(this_adjustment_project)] += float(eval(str(row[1].value).replace('=','')))
            else:
                print 'couldnt find matching key for row: %s %s --%s--' % (row[0].value, row[1].value, row[2].value)
                continue
        for key, value in iter(sorted(project_status.iteritems())):
            print '%s - %s' % (key, str(value))
        return project_status

    def generate_project_summary(self, code):
        dict_summary = {}
        summary_lines = []
        for item in self.get_sales_categories():
            dict_summary[str(item)] = 0.0
        for row in self.data_input:
            this_adjustment_project = row[2].value
            try:
                this_adjustment_project = this_adjustment_project.lower()
            except Exception as e:
                print 'ERROR generate_project_summery .lower()'
                continue
                placeholder = 0
            if this_adjustment_project in code:
                #save summary line
                date = str(row[0].value)
                amount = float(eval(str(row[1].value).replace('=','')))
                royalty = this_adjustment_project
                qty = str(row[3].value)
                category = str(row[4].value).lower()
                company = str(row[5].value)
                details = str(row[6].value)
                details_2 = str(row[7].value)
                summary_line = [date, amount, royalty, qty, category, company, details, details_2]
                summary_lines.append(summary_line)
                #adjust dict by amount
                dict_summary[category] += amount
        
                
    def get_royalty_status(self):
        royalty_codes = self.get_royalty_codes()
        royalty_status = {}
        for roy in royalty_codes:
            royalty_status[str(roy)] = 0.0
        for row in self.data_input:
            this_adjustment_project = row[2].value
            try:
                this_adjustment_project = this_adjustment_project.lower()
            except Exception as e:
                placeholder = 0
            found = False
            if str(this_adjustment_project) in royalty_status:
                royalty_status[str(this_adjustment_project)] += float(eval(str(row[1].value).replace('=','')))
            else:
                print 'couldnt find matching key for row: %s %s %s' % (row[0].value, row[1].value, row[2].value)
                continue
        for key, value in iter(sorted(royalty_status.iteritems())):
            print '%s - %s' % (key, str(value))
        return royalty_status

            #adjustments = self.data_input['B']
            #for index, item in adjustments:

    def print_payee_summary(self):
        project_status = self.get_project_status()
        royalty_status = self.get_royalty_status()
        payees = self.get_payees()
        sheet_row_master = 1
        wb_master = openpyxl.Workbook()
        ws_master = wb_master.active
        ws_master.title = "Master Summary"
        summary_of_payments = []
        for payee in payees:
            sheet_row = 1
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "All Projects Summary"
            summary_of_payments = []
            print '-----------------------------------------------'
            print payee
            for row in self.projects:
                if str(row[0].value).lower().strip() == payee:#this guy is on this project, what we owe him?
                    #first make sure that this is an actual payee, and not a project summary
                    if len(str(row[3].value)) < 2 or row[3].value is None:
                        #this is a project summary, not a payee
                        continue
                    #get project number and validate
                    catalog_number = str(row[2].value)
                    try:
                        catalog_number = catalog_number.lower()
                    except Exception as e:
                        placeholder = 0
                    if catalog_number not in project_status:
                        print 'Holy shit, this dude is on a project that doesn\'t even exist'
                        print catalog_number
                        continue
                    #what is this payee's percentage?
                    percent = float(row[5].value)
                    project_budget_status = float(project_status[catalog_number])
                    money_owed =  project_budget_status * percent
                    #get royalty code and validate
                    money_paid = 0
                    royalty_number = row[3].value
                    try:
                        royalty_number = royalty_number.lower()
                    except Exception as e:
                        placeholder = 0
                    if royalty_number not in royalty_status:
                        print 'Invalid royalty number or this person has never been paid - %s' % royalty_number
                    else:
                        money_paid = float(royalty_status[royalty_number])
                    money_owed_after_paid = money_owed + money_paid
                    summary_of_payments.append([str(payee),str(row[1].value),str(row[2].value),str(row[3].value),str(locale.currency(project_budget_status)),str(percent*100)+'%',str(locale.currency(money_owed)),str(locale.currency(-money_paid)),str(locale.currency(money_owed_after_paid))])
                    
                    #individual project workbooks
                    #generate project_summary
                    project_summary = self.generate_project_summary(catalog_number)
                    
                    sheet_name = str(row[1].value).replace(' ','_')
                    sheet_name = re.sub(r'\W+', '', sheet_name)
                    ws_project = wb.create_sheet('%s_%s' % (sheet_name, str(row[2].value)))
                    

                    
            print '|\t%s\t|\t%s\t|\t%s\t|\t%s\t|\t%s\t|\t%s\t|\t%s\t|\t%s\t|\t%s\t|' % ('Payee','Title','Catalog No', 'Code', 'Total', 'Percentage','Total Earned','Total Paid','Current Due')
            for index, col, in enumerate(('Payee','Title','Catalog No', 'Code', 'Total', 'Percentage','Total Earned','Total Paid','Current Due')):
                (ws.cell(row=sheet_row, column=index+1)).value = col
            sheet_row += 1

            for index, col, in enumerate(('Payee','Title','Catalog No', 'Code', 'Total', 'Percentage','Total Earned','Total Paid','Current Due')):
                (ws_master.cell(row=sheet_row_master, column=index+1)).value = col
            sheet_row_master += 1
            
            total_owed = 0
            for row in summary_of_payments:
                print '|\t%s\t|\t%s\t|\t%s\t|\t%s\t|\t%s\t|\t%s\t|\t%s\t|\t%s\t|\t%s\t|' % tuple(row) 
                print '--------------------------------------------------------------------------' * 2
                for index, col in enumerate(row):
                    (ws.cell(row=sheet_row, column=index+1)).value = col
                sheet_row += 1
                cash_me_outside = self.xfloat(row[-1].replace('$',''))
                if cash_me_outside > 0:
                    total_owed += cash_me_outside
            (ws.cell(row=sheet_row,column=8)).value = 'Total Due ->'
            #(ws.cell(row=sheet_row,column=9)).style = 'Currency' 
            (ws.cell(row=sheet_row,column=9)).value = str(locale.currency(total_owed))
            (ws.cell(row=sheet_row,column=9)).font = openpyxl.styles.Font(bold=True)
            sheet_row += 2
            print '-------------------------------------'
            wb.save(BASE_PATH + 'plaid_room/royalty_summaries/%s.xlsx' % (payee.replace(' ','-')))

            #master summary workbook
            total_owed = 0
            for row in summary_of_payments:
                print '|\t%s\t|\t%s\t|\t%s\t|\t%s\t|\t%s\t|\t%s\t|\t%s\t|\t%s\t|\t%s\t|' % tuple(row) 
                for index, col in enumerate(row):
                    (ws_master.cell(row=sheet_row_master, column=index+1)).value = col
                sheet_row_master += 1
                cash_me_outside = self.xfloat(row[-1].replace('$',''))
                if cash_me_outside > 0:
                    total_owed += cash_me_outside
            (ws_master.cell(row=sheet_row_master,column=8)).value = 'Total Due ->'
            #(ws.cell(row=sheet_row,column=9)).style = 'Currency' 
            (ws_master.cell(row=sheet_row_master,column=9)).value = str(locale.currency(total_owed))
            (ws_master.cell(row=sheet_row_master,column=9)).font = openpyxl.styles.Font(bold=True)
            sheet_row_master += 2            
            
        wb_master.save(BASE_PATH + 'plaid_room/royalty_summaries/MASTER_FOR_COLEMINE_EMPLOYEES.xlsx')
            
                    
                    
    def filter_non_numeric(self, str_):
        return self.non_decimal.sub('', str_)

    def xfloat(self, f):
        if (f is None) or (f == ''):
            return -1
        return float(f)
    
    def print_sheet_names(self):
        for sheet in self.wb.worksheets:
            print sheet


if __name__ == '__main__':
    books = ColemineBooks(sys.argv[1], sys.argv[2])
    #books.print_sheet_names()
    #books.get_sales_categories()
    #books.get_projects()
    #books.get_project_status()
    #books.get_payees()
    books.print_payee_summary()
