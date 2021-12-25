import xlrd
import xlsxwriter as out
from mat import Mat
import csv

def parseExcel(file,rownames=False):
    assert type(file) == str
    f=xlrd.open_workbook(file,on_demand=True)
    assert f.nsheets>0
    ws = f.sheet_by_index(0)

    #Tuple implementation
    if f.nsheets==1:
         #assert type(ws.cell)==type(xlrd.empty_cell)
        if rownames == False:
            cols = (ws.cell(0,numCols).value for numCols in range(ws.ncols))
            table = ((ws.cell(numRows,numCols).value for numRows in set(range(ws.nrows))-{0}) for numCols in range(ws.ncols))
            return (table,cols)
        else:
            cols = (ws.cell(0,numCols).value for numCols in set(range(ws.ncols))-{0})
            rows = (ws.cell(numRows,0).value for numRows in set(range(ws.nrows)) - {0})
            table = ((ws.cell(numRows,numCols).value for numRows in set(range(ws.nrows))-{0}) for numCols in set(range(ws.ncols))-{0})
            return (table,rows,cols)
    else: # nsheets>1
        print("multiple sheets detected, please finish implementation")
    f.close()
def parseExcelMat(file,rownames=False):
    assert type(file) == str
    f=xlrd.open_workbook(file,on_demand=True)
    assert f.nsheets>0
    ws = f.sheet_by_index(0)

#Set implementation
    if f.nsheets==1:
        cols=set()
        col2num={}
        #assert type(ws.cell)==type(xlrd.empty_cell)


        for numCols in range(ws.ncols):
            cols.add(ws.cell(0,numCols).value)
            col2num.update({ws.cell(0,numCols).value:numCols})
        if rownames==False:
            #Assuming that the rows are numCol-Vectors
            M= Mat((set(range(ws.nrows))-{0},cols),{(r,c):ws.cell(r,col2num[c]).value for r in set(range(ws.nrows))-{0} for c in cols if ws.cell(r,col2num[c]).value != xlrd.empty_cell.value}) ###
        else:
            rows=set()
            row2num={}
            cols.remove(ws.cell(0,0).value)
            #while ws.cell(numRows, 0).value != xlrd.empty_cell.value:
            for numRows in set(range(ws.nrows))-{0}:
                rows.add(ws.cell(numRows, 0).value)
                row2num.update({ws.cell(numRows,0).value:numRows})
            M=Mat((rows,cols),{(r,c):ws.cell(row2num[r],col2num[c]).value for r in rows for c in cols if ws.cell(row2num[r],col2num[c]).value != xlrd.empty_cell.value})
        return M
    else:
        print("n sheets>1, finish implementation.")

def write(s,file="untitled"):
    if not file.contains(".xlsx"):
        file+=".xlsx"
    wb=out.Workbook(file)

    for i in range(len(s)):
        ws=wb.add_worksheet()
        ##

def parsecsv(file,colnames=True,rownames=False):
	assert type(file)==str
	with open(file,newline='') as csvfile:
		r=csv.reader(csvfile,delimiter=',')
		f=dict()
		if colnames == True:
			cols=next(r)
			if rownames == True:
				cols.pop(0)
				d0=set()
				for row in r:
					d0.update({row[0]})
					for j in range(len(cols)):
						f.update({(row[0],cols[j]):row[j+1]})
			else:
				i=0
				for row in r:
					for j in range(len(cols)):
						f.update({(i,cols[j]):row[j]})
					i+=1
				d0=set(range(i))
			M=Mat((d0,set(cols)),f)
		else: #No colnames
			if rownames == True:
				d0=set()
				for row in r:
					d0.update({row[0]})
					for j in set(range(len(row)))-{len(row)-1}:
						f.update({(row[0],j):row[j+1]})
				M=Mat((d0,set(range(j))),f)
			else:
				i=0
				for row in r:
					for j in range(len(row)):
						f.update({(i,j):row[j]})
					i+=1
				M=Mat((set(range(i)),set(range(j))),f)
	return M


