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
        
        
        #print data_input
        #sheet_ranges = data_input['range names']
        #print sheet_ranges

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

    def print_project_status(self):
        project_codes = self.get_projects()
        project_status = {} #new dict
        for pro in project_codes:
            project_status[pro] = 0.0
        for row in self.data_input:
            this_adjustment_project = row[2].value
            print this_adjustment_project
            found = False
            for key in project_status:
                if str(key) in str(this_adjustment_project):
                    this_adjustment_project = key
                    found = True
                    break
            if found == False:
                print 'couldnt find matching key for row: %s %s %s' % (row[0].value, row[1].value, row[2].value)
                continue
            project_status[this_adjustment_project] += float(eval(str(row[1].value).replace('=','')))
        for key, value in project_status.iteritems():
            print '%s - %s' % (key, str(value))

            #adjustments = self.data_input['B']
            #for index, item in adjustments:
    
    def print_sheet_names(self):
        for sheet in self.wb.worksheets:
            print sheet


if __name__ == '__main__':
    books = ColemineBooks()
    books.print_sheet_names()
    books.get_sales_categories()
    books.get_projects()
    books.print_project_status()
