from json import dump,dumps
import os
import pandas as pd

os.chdir(os.path.dirname(os.path.abspath(__file__)))

M=pd.read_csv("../covidStates.csv")
z=zip(M['date'],M['state'],M['cases'],M['deaths'])
dat={yr:dict() for yr in set(M['date'])}

for date,s,c,d in zip(M['date'],M['state'],M['cases'],M['deaths']):
    dat[date].update({s:{'cases':c,'deaths':d}})

print(dat)


with open("../covidStates.json","w") as writef:
    dump(dat,writef)
