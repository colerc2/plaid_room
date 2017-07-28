import openpyxl
from config_stuff import *

class ColemineBooks():
    def __init__(self):
        self.wb = openpyxl.load_workbook(COLEMINE_BOOKS_FILE)
        self.data_input = self.wb.get_sheet_by_name(name = 'Data Input')
        self.projects = self.wb.get_sheet_by_name(name = 'Project & Royalties')
        
    def get_projects(self):
        #get all projects
        p = self.projects['C']

        projects_set = set()
        for row in p:
            try:
                projects_set.add(row.value.lower())
            except Exception as e:
                projects_set.add(row.value)
                print e
        sorted_projects = sorted(projects_set)
        for row in sorted_projects:
            print row
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
                print e
        sorted_royalty = sorted(royalty_set)
        return sorted_royalty
        
        #print data_input
        #sheet_ranges = data_input['range names']
        #print sheet_ranges

    def get_payees(self):
        p = self.projects['A']
        payees_set = set()

        for row in p:
            try:
                payees_set.add(row.value.lower().strip())
            except Exception as e:
                print 'couldnt add payee to list: %s - %s' % (str(row.value), e)
        sorted_payees = sorted(payees_set)
        for row in sorted_payees:
            print row
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
        for payee in payees:
            summary_of_payments = []
            print '-----------------------------------------------'
            print payee
            for row in self.projects:
                if str(row[0].value).lower().strip() == payee:#this guy is on this project, what we owe him
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
                    money_owed = float(project_status[catalog_number])
                    #get royalty code and validate
                    money_paid = 0
                    royalty_number = row[3].value
                    try:
                        royalty_number = royalty_number.lower()
                    except Exception as e:
                        placeholder = 0
                    if royalty_number not in royalty_status:
                        print 'Invalid royalty number or this person has never been paid'
                    else:
                        money_paid = float(royalty_status[royalty_number])
                    money_owed_after_paid = money_owed - money_paid
                    summary_of_payments.append([payee,row[1].value,row[2].value,row[3].value,money_owed,money_paid])
            for row in summary_of_payments:
                print row
            print '-------------------------------------'
                    
                    
                    
    
    def print_sheet_names(self):
        for sheet in self.wb.worksheets:
            print sheet


if __name__ == '__main__':
    books = ColemineBooks()
    books.print_sheet_names()
    books.get_sales_categories()
    books.get_projects()
    books.get_project_status()
    books.get_payees()
    books.print_payee_summary()
