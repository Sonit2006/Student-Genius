import xlsxwriter
import xlsxwriter.utility
import mysql.connector
from datetime import datetime
import pandas as pd
import configparser

#reading the current report
df = pd.read_excel('Report.xlsx')

#obtaining the quarter number
currentMonth = datetime.now().strftime("%m")
for i, num in enumerate([11, 1, 4]):
    if int(currentMonth) >= num and int(currentMonth) <= num+2:
        quarterNum = i+1
        break

#lists to store the points that are already present in the report
previous_quarter_points9 = []
previous_quarter_points10 = []
previous_quarter_points11 = []
previous_quarter_points12 = []

#appending them to the lists from the report
for quart in range(1, quarterNum):
    previous_quarter_points9.append("Unnamed: {}".format(2+quart-1))
for quart in range(1, quarterNum):
    previous_quarter_points10.append("Unnamed: {}".format(5+quarterNum+quart-1))
for quart in range(1, quarterNum):
    previous_quarter_points11.append("Unnamed: {}".format(8+2*quarterNum+quart-1))
for quart in range(1, quarterNum):
    previous_quarter_points12.append("Unnamed: {}".format(11+3*quarterNum+quart-1))
    
#gets all the student names, grades and points for that quarter from database
def fetch_table_data(table):
    

    config = configparser.ConfigParser()
    config.read("C:/Users/Sonit Maddineni/Documents/config.ini")
    cnx = mysql.connector.connect(
        host='localhost',
        database='nchs',
        user = config.get('mysql', 'user'),
        password = config.get('mysql', 'password')
    )

    cursor = cnx.cursor()

    cursor.execute('SELECT Name, Grade FROM nchs.track WHERE Grade = 9')
    header1 = [row[0] for row in cursor.description]
    rows1 = cursor.fetchall()

    cursor.execute('SELECT Name, Grade FROM nchs.track WHERE Grade = 10')
    header2 = [row[0] for row in cursor.description]
    rows2 = cursor.fetchall()
    
    cursor.execute('SELECT Name, Grade FROM nchs.track WHERE Grade = 11')
    header3 = [row[0] for row in cursor.description]
    rows3 = cursor.fetchall()

    cursor.execute('SELECT Name, Grade FROM nchs.track WHERE Grade = 12')
    header4 = [row[0] for row in cursor.description]
    rows4 = cursor.fetchall()

    #Obtaining points for this quarter from the database
    cursor.execute('SELECT Points FROM nchs.track WHERE Grade = 9')
    grade9Points = [row[0] for row in cursor]

    cursor.execute('SELECT Points FROM nchs.track WHERE Grade = 10')
    grade10Points = [row[0] for row in cursor]

    cursor.execute('SELECT Points FROM nchs.track WHERE Grade = 11')
    grade11Points = [row[0] for row in cursor]

    cursor.execute('SELECT Points FROM nchs.track WHERE Grade = 12')
    grade12Points = [row[0] for row in cursor]

    # Closing connection
    cnx.close()

    return header1, rows1, header2, rows2, header3, rows3, header4, rows4, grade9Points, grade10Points, grade11Points, grade12Points


def export(table_name):
    # Create an new Excel file and add a worksheet.
    workbook = xlsxwriter.Workbook(table_name + '.xlsx')
    worksheet = workbook.add_worksheet('MENU')
    wrksht9 = workbook.add_worksheet('Grade 9 report')
    wrksht10 = workbook.add_worksheet('Grade 10 report')
    wrksht11 = workbook.add_worksheet('Grade 11 report')
    wrksht12 = workbook.add_worksheet('Grade 12 report')

    #Adding charts for each grade in each sheet and setting title and labels
    gradeGraph9 = workbook.add_chart({'type':'column'})
    gradeGraph10 = workbook.add_chart({'type':'column'})
    gradeGraph11 = workbook.add_chart({'type':'column'})
    gradeGraph12 = workbook.add_chart({'type':'column'})

    gradeGraph9.set_title({'name': 'Total points for grade 9'})
    gradeGraph9.set_x_axis({'name': 'Quarters'})
    gradeGraph9.set_y_axis({'name': 'Points'})

    gradeGraph10.set_title({'name': 'Total points for grade 10'})
    gradeGraph10.set_x_axis({'name': 'Quarters'})
    gradeGraph10.set_y_axis({'name': 'Points'})

    gradeGraph11.set_title({'name': 'Total points for grade 11'})
    gradeGraph11.set_x_axis({'name': 'Quarters'})
    gradeGraph11.set_y_axis({'name': 'Points'})

    gradeGraph12.set_title({'name': 'Total points for grade 12'})
    gradeGraph12.set_x_axis({'name': 'Quarters'})
    gradeGraph12.set_y_axis({'name': 'Points'})


    # Create style for cells
    header_cell_format = workbook.add_format({'bold': True, 'border': True, 'bg_color': 'yellow'})
    body_cell_format = workbook.add_format({'border': True})
    merge_format = workbook.add_format({
    'bold': 1,
    'border': 1,
    'align': 'center',
    'valign': 'vcenter',
    'fg_color': 'yellow',
    'font_size': 20})
    merge_format2 = workbook.add_format({
    'bold': 1,
    'border': 1,
    'align': 'center',
    'valign': 'vcenter',
    'fg_color': 'black',
    'font_size': 13,
    'font_color':'white'})


# Merging cells.
    worksheet.merge_range('E1:J2', 'Report for this Quarter', merge_format)
    wrksht9.merge_range('E1:J2', 'Report for Grade 9', merge_format)
    wrksht10.merge_range('E1:J2', 'Report for Grade 10', merge_format)
    wrksht11.merge_range('E1:J2', 'Report for Grade 11', merge_format)
    wrksht12.merge_range('E1:J2', 'Report for Grade 12', merge_format)

    worksheet.merge_range(6, 0, 7, 1+quarterNum, 'Grade 9', merge_format2)
    worksheet.merge_range(6, 3+quarterNum, 7, 4+2*quarterNum, 'Grade 10', merge_format2)
    worksheet.merge_range(6, 6+2*quarterNum, 7, 7+3*quarterNum, 'Grade 11', merge_format2)
    worksheet.merge_range(6, 9+3*quarterNum, 7, 10+4*quarterNum, 'Grade 12', merge_format2)

    wrksht9.merge_range(6, 1, 7, 2+quarterNum, 'Grade 9', merge_format2)
    wrksht10.merge_range(6, 1, 7, 2+quarterNum, 'Grade 10', merge_format2)
    wrksht11.merge_range(6, 1, 7, 2+quarterNum, 'Grade 11', merge_format2)
    wrksht12.merge_range(6, 1, 7, 2+quarterNum, 'Grade 12', merge_format2)

    # worksheet.freeze_panes()
    header1, rows1, header2, rows2, header3, rows3, header4, rows4, grade9points, grade10points, grade11points, grade12points = fetch_table_data(table_name)
    worksheet.set_column(0,0, width = 25)
    worksheet.set_column(3+quarterNum, 3+quarterNum, width = 25)
    worksheet.set_column(6+2*quarterNum,6+2*quarterNum, width = 25)
    worksheet.set_column(9+3*quarterNum, 9+3*quarterNum, width = 25)

    wrksht9.set_column(1,1, width = 25)
    wrksht10.set_column(1,1, width = 25)
    wrksht11.set_column(1,1, width = 25)
    wrksht12.set_column(1,1, width = 25)

    #writes all the name, grade and point to the excel file.
    def make_table(head, rows, row_index, column_index, ind):
        graphList = [gradeGraph9, gradeGraph10, gradeGraph11, gradeGraph12]
        gradeSheets = [wrksht9, wrksht10, wrksht11, wrksht12]
        qHeaders = ['Q{}'.format(i) for i in range(1, quarterNum+1)]
        gradePoints = [grade9points, grade10points, grade11points, grade12points]
        previousPoints = [previous_quarter_points9, previous_quarter_points10, previous_quarter_points11, previous_quarter_points12]
        col = column_index
        #gradecol is for individual grade reports
        gradeCol = 1


        for column_name in head + qHeaders:
            worksheet.write(row_index, col, column_name, header_cell_format)
            gradeSheets[ind].write(row_index, gradeCol, column_name, header_cell_format)
            col += 1
            gradeCol += 1

        #writing names and grades
        row_index += 1
        rowStart = row_index
        for row in rows :
            col = column_index
            gradeCol = 1
            for column in row:
                worksheet.write(row_index, col, column, body_cell_format)
                gradeSheets[ind].write(row_index, gradeCol, column, body_cell_format)
                col += 1
                gradeCol += 1
            row_index += 1
        
        row_index += 1
        worksheet.write(row_index, col-1, "Total:")

        #rewriting the points that were previously there in the sheet
        for i in df[previousPoints[ind]].iloc[9:].dropna():
            rowForPoints = rowStart
            for point in df[previousPoints[ind]][i].iloc[8:].dropna()[:-1]:
                worksheet.write(rowForPoints, col, point, body_cell_format)
                gradeSheets[ind].write(rowForPoints, gradeCol, point, body_cell_format)
                rowForPoints += 1
            
            rowForPoints += 1
            col_letter = xlsxwriter.utility.xl_col_to_name(col)
            col_letter2 = xlsxwriter.utility.xl_col_to_name(gradeCol)
            worksheet.write_formula(rowForPoints, col, '=SUM(' + col_letter + '10:' + col_letter + str(rowForPoints - 1) + ')')
            gradeSheets[ind].write_formula(rowForPoints, gradeCol, '=SUM(' + col_letter2 + '10:' + col_letter2 + str(rowForPoints - 1) + ')')
            col += 1
            gradeCol+=1
        
        

        #points for this quarter
        rowForPoints = rowStart
        for point in gradePoints[ind]:
            worksheet.write(rowForPoints, col, point, body_cell_format)
            gradeSheets[ind].write(rowForPoints, gradeCol, point, body_cell_format)
            rowForPoints += 1
        col_letter = xlsxwriter.utility.xl_col_to_name(gradeCol)
        graphList[ind].add_series({'values': '=\'Grade ' + str(ind+9) + ' report\'!$D$' + str(rowForPoints+2) + ':$' + col_letter + '$' + str(rowForPoints+2), 'name':'Quarter '+str(quarterNum), 'categories':[f'Grade {ind+9} report', 8,3,8,5], 'fill':{'color':'red'}})
        
        rowForPoints += 1
        col_letter = xlsxwriter.utility.xl_col_to_name(col)
        col_letter2 = xlsxwriter.utility.xl_col_to_name(gradeCol)
        worksheet.write_formula(rowForPoints, col, '=SUM(' + col_letter + '10:' + col_letter + str(rowForPoints - 1) + ')')
        gradeSheets[ind].write_formula(rowForPoints, gradeCol, '=SUM(' + col_letter2 + '10:' + col_letter2 + str(rowForPoints - 1) + ')')

    
    #inserting charts
    wrksht9.insert_chart(6, col=11, chart=gradeGraph9)
    wrksht10.insert_chart(6, col=11, chart=gradeGraph10)
    wrksht11.insert_chart(6, col=11, chart=gradeGraph11)
    wrksht12.insert_chart(6, col=11, chart=gradeGraph12)
    
    
    make_table(header1, rows1, 8, 0, 0)
    make_table(header2, rows2, 8, 3+quarterNum, 1)
    make_table(header3, rows3, 8, 6+2*quarterNum, 2)
    make_table(header4, rows4, 8, 9+3*quarterNum, 3)

    workbook.close()

#exporting to excel with the same name.
export('Report')
