#!/usr/bin/python

import datetime
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
                #print e
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
                #print 'This is a summary, not a payee: %s - %s' % (str(row[0].value),str(row[1].value))
                continue
            try:
                payees_set.add(row[0].value.lower().strip())
            except Exception as e:
                print 'couldnt add payee to list: %s - %s' % (str(row[0].value), e)
        sorted_payees = sorted(payees_set)
        #print '--------------------------'
        #for row in sorted_payees:
            #print row
        #print '--------------------------'
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
        #print sales_categories
        return sales_categories

    def get_project_status(self):
        project_codes = self.get_projects()
        royalty_codes = self.get_royalty_codes()
        project_status = {} #new dict
        for pro in project_codes:
            project_status[str(pro)] = 0.0
        for row in self.data_input:
            this_adjustment_project = row[2].value
            try:
                this_adjustment_project = this_adjustment_project.lower()
            except Exception as e:
                placeholder = 0
            #print '--%s--' % this_adjustment_project
            found = False
            if str(this_adjustment_project) in project_status:
                project_status[str(this_adjustment_project)] += float(eval(str(row[1].value).replace('=','')))
            else:
                if str(this_adjustment_project) not in royalty_codes:
                    print 'couldnt find matching key for row: %s %s --%s--' % (row[0].value, row[1].value, row[2].value)
                continue
        #for key, value in iter(sorted(project_status.iteritems())):
        #    print '%s - %s' % (key, str(value))
        return project_status

    def generate_project_summary(self, code):
        dict_summary = {}
        dict_qty = {}
        summary_lines = []
        for item in self.get_sales_categories():
            dict_summary[str(item)] = 0.0
            dict_qty[str(item)] = 0
        for row in self.data_input:
            this_adjustment_project = row[2].value
            try:
                this_adjustment_project = this_adjustment_project.lower()
            except Exception as e:
                placeholder = 0
            if code == str(this_adjustment_project):# or (('r%s'%code) == str(this_adjustment_project)):
                #print row
                #save summary line
                date = row[0].value
                amount = float(eval(str(row[1].value).replace('=','')))
                royalty = this_adjustment_project
                qty = row[3].value
                category = str(row[4].value).lower()
                company = ''
                try:
                    company = self.xstr(row[5].value)
                except Exception as e:
                    placeholder = 0
                    #continue
                    #print '**********\n' * 5
                    #print row[5].value
                details = str(row[6].value)
                details_2 = str(row[7].value)
                summary_line = [date, amount, royalty, qty, category, company, details, details_2]
                summary_lines.append(summary_line)
                #adjust dict by amount
                dict_summary[category] += amount
                #adjust qty if applicable
                if qty is not None:
                    try:
                        qty = int(qty)
                        dict_qty[category] += qty
                    except Exception as e:
                        continue
        return (dict_summary, dict_qty, summary_lines)

    def generate_quarterly_project_summary(self, code, year, quarter):
        dict_summary = {}
        dict_qty = {}
        summary_lines = []
        for item in self.get_sales_categories():
            dict_summary[str(item)] = 0.0
            dict_qty[str(item)] = 0
        for row in self.data_input:
            this_adjustment_project = row[2].value
            try:
                this_adjustment_project = this_adjustment_project.lower()
            except Exception as e:
                placeholder = 0
            if code == str(this_adjustment_project):# or (('r%s'%code) == str(this_adjustment_project)):
                #print row
                #save summary line
                date = row[0].value
                #date_ = openpyxl.utils.datetime.from_excel(date)
                #date_ = datetime.datetime(date)
                #print date.month
                #print self.quarter
                #print
                #print date.year
                #print self.year
                #print
                if (((date.month-1)//3)+1) != int(quarter):
                    continue
                if date.year != int(year):
                    continue
                amount = float(eval(str(row[1].value).replace('=','')))
                royalty = this_adjustment_project
                qty = str(row[3].value)
                category = str(row[4].value).lower()
                company = ''
                details = ''
                details_2 = ''
                try:
                    company = self.xstr(row[5].value)
                    details = str(row[6].value)
                    details_2 = str(row[7].value)
                except Exception as e:
                    placeholder = 0
                summary_line = [date, amount, royalty, qty, category, company, details, details_2]
                summary_lines.append(summary_line)
                #adjust dict by amount
                dict_summary[category] += amount
                #adjust qty if applicable
                if qty is not None:
                    try:
                        qty = int(qty)
                        dict_qty[category] += qty
                    except Exception as e:
                        continue
        return (dict_summary, dict_qty, summary_lines)
    
    def get_royalty_status(self):
        royalty_codes = self.get_royalty_codes()
        project_codes = self.get_projects()
        project_codes = map(str, project_codes)
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
                if str(this_adjustment_project) not in project_codes:
                    print 'couldnt find matching key for row: %s %s %s' % (row[0].value, row[1].value, row[2].value)
                    #print project_codes
                continue
        #for key, value in iter(sorted(royalty_status.iteritems())):
        #    print '%s - %s' % (key, str(value))
        return royalty_status

            #adjustments = self.data_input['B']
            #for index, item in adjustments:
    def correct_column_widths(self, wb):
        for sheet in wb.worksheets:
            for col in ['A','B','C','D','E','F','G']:
                sheet_col = sheet[col]
                list_of_lengths = []
                for row in sheet_col:
                    try:
                        list_of_lengths.append(len(row.value))
                    except Exception as e:
                        placeholder = 0
                max_length = max(list_of_lengths)+2
                sheet.column_dimensions[col].width = max_length
            
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
            #print '-----------------------------------------------'
            #print payee
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
                    summary_of_payments.append([str(payee),str(row[1].value),str(row[2].value),str(row[3].value),project_budget_status,str(percent*100)+'%',money_owed,-money_paid,money_owed_after_paid])
                    
                    #individual project workbooks
                    #generate project_summary
                    project_summary = self.generate_project_summary(catalog_number)
                    
                    sheet_name = str(row[1].value).replace(' ','_')
                    sheet_name = re.sub(r'\W+', '', sheet_name)
                    ws_project = wb.create_sheet('%s_%s' % (sheet_name, str(row[2].value)))
                    project_sheet_row = 1
                    (ws_project.cell(row=project_sheet_row, column=1)).value = 'ALL TIME SUMMARY'
                    (ws_project.cell(row=project_sheet_row, column=1)).font = openpyxl.styles.Font(bold=True)
                    project_sheet_row += 1
                    for index, col, in enumerate(('Category', 'Debit/Credit', 'Quantity (if applicable)')):
                        (ws_project.cell(row=project_sheet_row, column=index+1)).value = col
                        (ws_project.cell(row=project_sheet_row, column=index+1)).font = openpyxl.styles.Font(bold=True)
                    project_sheet_row += 1
                    total_sold = 0
                    project_budget = 0
                    #for key, value in sorted(project_summary[0].iteritems()):
                    for key, value in sorted(project_summary[0].items(), key=lambda x: x[1],reverse=True):
                        if float(value) == 0:
                            continue
                        project_budget += value
                        total_sold += (project_summary[1])[key]
                        (ws_project.cell(row=project_sheet_row, column=1)).value = str(key).title()
                        (ws_project.cell(row=project_sheet_row, column=2)).value = value
                        (ws_project.cell(row=project_sheet_row, column=2)).number_format = '$#,##0.00;[Red]-$#,##0.00'
                        (ws_project.cell(row=project_sheet_row, column=3)).value = (project_summary[1])[key]
                        project_sheet_row += 1
                    (ws_project.cell(row=project_sheet_row, column=1)).value = 'Totals'
                    (ws_project.cell(row=project_sheet_row, column=1)).font = openpyxl.styles.Font(bold=True)
                    (ws_project.cell(row=project_sheet_row, column=2)).value = project_budget
                    (ws_project.cell(row=project_sheet_row, column=2)).font = openpyxl.styles.Font(bold=True)
                    (ws_project.cell(row=project_sheet_row, column=2)).number_format = '$#,##0.00;[Red]-$#,##0.00'
                    (ws_project.cell(row=project_sheet_row, column=3)).value = total_sold
                    (ws_project.cell(row=project_sheet_row, column=3)).font = openpyxl.styles.Font(bold=True)

                    #quarterly summary ---------------
                    num_quarters = 4
                    pairs = []
                    year = int(self.year)
                    quarter = int(self.quarter)
                    for ii in range(num_quarters):
                        if quarter == 0:
                            quarter = 4
                            year -= 1
                        pairs.append([year,quarter])
                        quarter -= 1
                    for pair in pairs:
                    
                        project_quarterly_summary = self.generate_quarterly_project_summary(catalog_number,int(pair[0]),int(pair[1]))
                    
                        project_sheet_row += 2
                        (ws_project.cell(row=project_sheet_row, column=1)).value = '%s Q%s SUMMARY' % (str(pair[0]), str(pair[1]))
                        (ws_project.cell(row=project_sheet_row, column=1)).font = openpyxl.styles.Font(bold=True)
                        project_sheet_row += 1
                        for index, col, in enumerate(('Category', 'Debit/Credit', 'Quantity (if applicable)')):
                            (ws_project.cell(row=project_sheet_row, column=index+1)).value = col
                            (ws_project.cell(row=project_sheet_row, column=index+1)).font = openpyxl.styles.Font(bold=True)
                        project_sheet_row += 1
                        total_sold = 0
                        project_budget = 0
                        #for key, value in sorted(project_summary[0].iteritems()):
                        for key, value in sorted(project_quarterly_summary[0].items(), key=lambda x: x[1],reverse=True):
                            if float(value) == 0:
                                continue
                            project_budget += value
                            total_sold += (project_quarterly_summary[1])[key]
                            (ws_project.cell(row=project_sheet_row, column=1)).value = str(key).title()
                            (ws_project.cell(row=project_sheet_row, column=2)).value = value
                            (ws_project.cell(row=project_sheet_row, column=2)).number_format = '$#,##0.00;[Red]-$#,##0.00'
                            (ws_project.cell(row=project_sheet_row, column=3)).value = (project_quarterly_summary[1])[key]
                            project_sheet_row += 1
                        (ws_project.cell(row=project_sheet_row, column=1)).value = 'Totals'
                        (ws_project.cell(row=project_sheet_row, column=1)).font = openpyxl.styles.Font(bold=True)
                        (ws_project.cell(row=project_sheet_row, column=2)).value = project_budget
                        (ws_project.cell(row=project_sheet_row, column=2)).font = openpyxl.styles.Font(bold=True)
                        (ws_project.cell(row=project_sheet_row, column=2)).number_format = '$#,##0.00;[Red]-$#,##0.00'
                        (ws_project.cell(row=project_sheet_row, column=3)).value = total_sold
                        (ws_project.cell(row=project_sheet_row, column=3)).font = openpyxl.styles.Font(bold=True)


                    
                    
                    #all the data ------------
                    project_sheet_row += 3
                    for index, col, in enumerate(('Date', 'Credit/Debit', 'Royalty', 'Qty', 'Category','Company','Details','Details 2')):
                        (ws_project.cell(row=project_sheet_row, column=index+1)).value = col
                        (ws_project.cell(row=project_sheet_row, column=index+1)).font = openpyxl.styles.Font(bold=True)
                    project_sheet_row += 1
                    for row_ in reversed(project_summary[2]):
                        for index, col in enumerate(row_):
                            (ws_project.cell(row=project_sheet_row, column=index+1)).value = col
                            if index == 0:
                                (ws_project.cell(row=project_sheet_row, column=index+1)).number_format = 'm/d/yyyy;@'
                                #(ws_project.cell(row=project_sheet_row, column=index+1)).number_format = '[$-409]m/d/yy h:mm AM/PM;@'
                            if index == 1:
                                (ws_project.cell(row=project_sheet_row, column=index+1)).number_format = '$#,##0.00;[Red]-$#,##0.00'
                            if index == 4:
                                (ws_project.cell(row=project_sheet_row, column=index+1)).value = col.title()
                                
                                
                        project_sheet_row += 1

                    
            #print '|\t%s\t|\t%s\t|\t%s\t|\t%s\t|\t%s\t|\t%s\t|\t%s\t|\t%s\t|\t%s\t|' % ('Payee','Title','Catalog No', 'Code', 'Total', 'Percentage','Total Earned','Total Paid','Current Due')
            for index, col, in enumerate(('Payee','Title','Catalog No', 'Code', 'Project Status', 'Percentage','Total Earned','Total Paid','Current Due')):
                (ws.cell(row=sheet_row, column=index+1)).value = col
                (ws.cell(row=sheet_row, column=index+1)).font = openpyxl.styles.Font(bold=True)
            sheet_row += 1

            for index, col, in enumerate(('Payee','Title','Catalog No', 'Code', 'Project Status', 'Percentage','Total Earned','Total Paid','Current Due')):
                (ws_master.cell(row=sheet_row_master, column=index+1)).value = col
            sheet_row_master += 1
            
            total_owed = 0
            for row in summary_of_payments:
                #print '|\t%s\t|\t%s\t|\t%s\t|\t%s\t|\t%s\t|\t%s\t|\t%s\t|\t%s\t|\t%s\t|' % tuple(row) 
                #print '--------------------------------------------------------------------------' * 2
                for index, col in enumerate(row):
                    if isinstance(col, str):
                        (ws.cell(row=sheet_row, column=index+1)).value = col.title()
                    else:
                        (ws.cell(row=sheet_row, column=index+1)).value = col                        
                    if (index+1) in [5, 7, 8, 9]:#rows with $$ formatting needed
                        (ws.cell(row=sheet_row, column=index+1)).number_format = '$#,##0.00;[Red]-$#,##0.00'
                        if (index+1) in [7,9]:
                            if col < 0:
                                (ws.cell(row=sheet_row, column=index+1)).value = 0                   
                                
                sheet_row += 1
                #cash_me_outside = self.xfloat(row[-1].replace('$',''))
                cash_me_outside = row[-1]
                if cash_me_outside > 0:
                    total_owed += cash_me_outside
            (ws.cell(row=sheet_row,column=8)).value = 'Sum Of Projects With Royalties Owed'
            #(ws.cell(row=sheet_row,column=9)).style = 'Currency' 
            (ws.cell(row=sheet_row,column=9)).value = str(locale.currency(total_owed))
            (ws.cell(row=sheet_row,column=9)).font = openpyxl.styles.Font(bold=True)
            sheet_row += 2
            #print '-------------------------------------'
            self.correct_column_widths(wb)
            wb.save(BASE_PATH + 'plaid_room/royalty_summaries/%s.xlsx' % (payee.replace(' ','-')))

            #master summary workbook
            total_owed = 0
            for row in summary_of_payments:
                #print '|\t%s\t|\t%s\t|\t%s\t|\t%s\t|\t%s\t|\t%s\t|\t%s\t|\t%s\t|\t%s\t|' % tuple(row) 
                for index, col in enumerate(row):
                    (ws_master.cell(row=sheet_row_master, column=index+1)).value = col
                    if (index+1) in [5, 7, 8, 9]:#rows with $$ formatting needed
                        (ws_master.cell(row=sheet_row_master, column=index+1)).number_format = '$#,##0.00;[Red]-$#,##0.00'
                sheet_row_master += 1
                #cash_me_outside = self.xfloat(row[-1].replace('$',''))
                cash_me_outside = row[-1]
                if cash_me_outside > 0:
                    total_owed += cash_me_outside
            (ws_master.cell(row=sheet_row_master,column=8)).value = 'Sum Of Projects With Royalties Owed'
            (ws_master.cell(row=sheet_row_master,column=8)).font = openpyxl.styles.Font(bold=True)
            #(ws.cell(row=sheet_row,column=9)).style = 'Currency' 
            #(ws_master.cell(row=sheet_row_master,column=9)).value = str(locale.currency(total_owed))
            (ws_master.cell(row=sheet_row_master,column=9)).value = total_owed
            (ws_master.cell(row=sheet_row_master,column=9)).font = openpyxl.styles.Font(bold=True)
            (ws_master.cell(row=sheet_row_master,column=9)).number_format = '$#,##0.00;[Red]-$#,##0.00'
            sheet_row_master += 2
            self.correct_column_widths(wb_master)
            
        wb_master.save(BASE_PATH + 'plaid_room/royalty_summaries/MASTER_FOR_COLEMINE_EMPLOYEES.xlsx')
            
                    
                    
    def filter_non_numeric(self, str_):
        return self.non_decimal.sub('', str_)

    def xfloat(self, f):
        if (f is None) or (f == ''):
            return -1
        return float(f)

    def filter_unprintable(self, str_):
        return filter(lambda x: x in string.printable, str_)

    
    def print_sheet_names(self):
        for sheet in self.wb.worksheets:
            print sheet

    def xstr(self,s):
        if s is None:
            return ''
        return str(s.encode('utf-8'))



if __name__ == '__main__':
    books = ColemineBooks(sys.argv[1], sys.argv[2])
    #books.print_sheet_names()
    #books.get_sales_categories()
    #books.get_projects()
    #books.get_project_status()
    #books.get_payees()
    books.print_payee_summary()
