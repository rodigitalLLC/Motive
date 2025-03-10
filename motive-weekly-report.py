import sys
import pandas
import datetime

today = datetime.date.today()
today_formatted_date = today.strftime("%Y-%m-%d")

# TODO
# remove the cancelled cases from the open cases and remove the future cases from the open cases.
# also create a new sheet for the open only cases
# need to filter the cut outs and do the open cases last.

# database

# required columns: Type,EmployeeID,Last Name,First Name,Title,Work State,PT/FT,DOB,Gender,Exemption Status,Employment Status,Hire Date,Service Date
#if len(sys.argv)!=3:
  #print ("Usage: {} {} {}".format(sys.argv[0],"<input xlsx sheet>"))
  #sys.exit()

xl=pandas.read_csv(sys.argv[1],parse_dates=['Days in Case Start Date','Days in Case End Date','Days in Case Last Modified Date'],
                   usecols=['Case Number','Employee Number','Employee Last, First Name','Days in Case Start Date','Days in Case End Date','case_type','Case Reason','Case Determination','case_status',
                            'Case Eligible Policies','Days in Case Last Modified Date'])
xls=xl.astype(str)
# drop the cancelled cases
xls = xls.drop(xls.loc[xls['case_status']=='Canceled'].index) 

open_cases_df=xls[xls['case_status']=='Open']
closed_cases_df=xls[xls['case_status']=='Closed']
# future cases
fc_df=xls.copy()
fc_df['Days in Case Start Date'] = pandas.to_datetime(fc_df['Days in Case Start Date'])
future_cases_df=fc_df[fc_df['Days in Case Start Date']>today_formatted_date]

open_denied_df=open_cases_df[open_cases_df['Case Determination']=='Denied']
# if there are denied cases that are also open, then we need to remove them from the open cases
if[len(open_denied_df)>0]:
  #open_cases_df=xls[xls['Case Determination']!= 'Denied']
  open_cases_df=open_cases_df[open_cases_df['Case Determination']!= 'Denied']

# if there are future cases that are also open, then we need to remove them from the open cases
if[len(future_cases_df)>0]:
  open_cases_df=open_cases_df[open_cases_df['Days in Case Start Date']<=today_formatted_date]

# future cases has a start date that is formatted with time stamp
#future_cases_df['Days in Case Start Date']=future_cases_df['Days in Case Start Date'].dt.strftime('%Y-%m-%d')
#future_cases_df['Days in Case Start Date']=future_cases_df['Days in Case Start Date'].dt.strftime('%Y-%m-%d')
future_cases_df['Days in Case Start Date']=future_cases_df['Days in Case Start Date'].dt.strftime('%m/%d/%Y')
future_cases_df['Days in Case End Date'] = pandas.to_datetime(future_cases_df['Days in Case End Date']).dt.strftime('%m/%d/%Y')
future_cases_df['Days in Case Last Modified Date']=pandas.to_datetime(future_cases_df['Days in Case Last Modified Date']).dt.strftime('%m/%d/%Y')

open_cases_df['Days in Case Start Date']=pandas.to_datetime(open_cases_df['Days in Case Start Date']).dt.strftime('%m/%d/%Y')
open_cases_df['Days in Case End Date']=pandas.to_datetime(open_cases_df['Days in Case End Date']).dt.strftime('%m/%d/%Y')
open_cases_df['Days in Case Last Modified Date']=pandas.to_datetime(open_cases_df['Days in Case End Date']).dt.strftime('%m/%d/%Y')

open_denied_df['Days in Case Start Date']=pandas.to_datetime(open_denied_df['Days in Case Start Date']).dt.strftime('%m/%d/%Y')
open_denied_df['Days in Case End Date']=pandas.to_datetime(open_denied_df['Days in Case End Date']).dt.strftime('%m/%d/%Y')
open_denied_df['Days in Case Last Modified Date']=pandas.to_datetime(open_denied_df['Days in Case End Date']).dt.strftime('%m/%d/%Y')

closed_cases_df['Days in Case Start Date']=pandas.to_datetime(closed_cases_df['Days in Case Start Date']).dt.strftime('%m/%d/%Y')
closed_cases_df['Days in Case End Date']=pandas.to_datetime(closed_cases_df['Days in Case End Date']).dt.strftime('%m/%d/%Y')
closed_cases_df['Days in Case Last Modified Date']=pandas.to_datetime(closed_cases_df['Days in Case End Date']).dt.strftime('%m/%d/%Y')

with pandas.ExcelWriter('open_cases.xlsx') as writer:  
  open_cases_df.to_excel(writer,sheet_name='Open Cases',index=False)
  closed_cases_df.to_excel(writer,sheet_name='Closed',index=False)
  open_denied_df.to_excel(writer,sheet_name='Open-Denied',index=False)
  future_cases_df.to_excel(writer,sheet_name='Future',index=False)