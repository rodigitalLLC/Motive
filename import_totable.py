import sys
import pandas
import sqlite3


# main

df=pandas.read_csv(sys.argv[1])
#df=pandas.read_(sys.argv[1],sep='|')
con = sqlite3.connect(sys.argv[2])
df.to_sql(sys.argv[3],con,if_exists='replace')