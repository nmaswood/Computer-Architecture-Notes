import openpyxl as o
import pandas as pd

FIRST_SHEET = 'colorado_2016_2017.xlsx'

def get_number_of_schools(sheet):

    SCHOOL_OFFSET = 6
    i = 0

    while sheet[SCHOOL_OFFSET + i][0].value is not None:
        i +=1

    return i

def create_day_dict():
    return {
        'no_school':  0,
        'first_and_last': 0,
        'half': 0,
        'other': 0
    }

def how_many_days_off_for_date(sheet, date):

    DATE_OFFSET = 0xdeadbeef

    return 0 

def process_sheet(sheet):

    DATE_ROW = 4
    DATE_OFFSET = 4
    
    # first couple rows have no information so we slice them out

    dates_row = s[DATE_ROW][DATE_OFFSET:]

    return

def process_workbook(name):

    wb = o.load_workbook(name, data_only = True)
    relevant_sheets = [sheet for sheet in wb.worksheets if '_' not in sheet.title]

    s = relevant_sheets[0]

    DATE_ROW = 4
    DATE_OFFSET = 4
    dates_row = s[DATE_ROW][DATE_OFFSET:]

    percentage_row = s[46][8]
    #print( help(percentage_row))
    SCHOOL_OFFSET = 0
    fuck = s[6]
    print(fuck[0].value)

    foo = get_number_of_schools(s)
    print (foo)


    return relevant_sheets

process_workbook(FIRST_SHEET)