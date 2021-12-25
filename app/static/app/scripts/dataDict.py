from parseExcel import parsecsv
from json import dump
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
M=parsecsv("../covidStates.csv",rownames=True)
print('Alabama' in M.colVec('state').f.values())
dat={year:dict() for year in M.D[0]}
for r in M.D[0]:
    
    dat[r].update({M[r,'state']:{'tests':M[r,'fips'],'cases':M[r,'cases'],'deaths':M[r,'deaths']}})
#print(False in {dat[year]})
#print('Alabama' in )
print(dat)
for r in M.D[0]:
    print(str('Alabama' in dat[r])+" "+r)
with open("../covidStates.json","w") as writef:
    dump(dat,writef)