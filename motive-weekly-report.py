import sys
import pandas
import datetime

today = datetime.date.today()
today_formatted_date = today.strftime("%Y-%m-%d")
#today_formatted_date = today.strftime("%m-%d-%Y")

# TODO
# remove the nan values from the dataframes 
# fix the date being see as a string in the excel sheet


#if len(sys.argv)!=3:
  #print ("Usage: {} {} {}".format(sys.argv[0],"<input xlsx sheet>"))
  #sys.exit()

# set up the output file
writer = pandas.ExcelWriter('opencases.xlsx', engine='xlsxwriter')

xl=pandas.read_csv(sys.argv[1],parse_dates=['Case Start Date','Case End Date','Last Modified Date'],
                   usecols=['Case Number','Employee Number','Employee Last, First Name','Case Start Date','Case End Date','FMLA Exhaust Date','case_type','Case Reason','Case Determination','case_status',
                            'Case Eligible Policies','Last Modified Date'])
xls=xl.astype(str)
# drop the cancelled cases
xls = xls.drop(xls.loc[xls['case_status']=='Canceled'].index) 

open_cases_df=xls[xls['case_status']=='Open']
closed_cases_df=xls[xls['case_status']=='Closed']
# future cases
fc_df=xls.copy()
fc_df['Case Start Date'] = pandas.to_datetime(fc_df['Case Start Date'])
future_cases_df=fc_df[fc_df['Case Start Date']>today_formatted_date]

open_denied_df=open_cases_df[open_cases_df['Case Determination']=='Denied']
# if there are denied cases that are also open, then we need to remove them from the open cases
if[len(open_denied_df)>0]:
  #open_cases_df=xls[xls['Case Determination']!= 'Denied']
  open_cases_df=open_cases_df[open_cases_df['Case Determination']!= 'Denied']

# if there are future cases that are also open, then we need to remove them from the open cases
if[len(future_cases_df)>0]:
  open_cases_df=open_cases_df[open_cases_df['Case Start Date']<=today_formatted_date]

# future cases has a start date that is formatted with time stamp
#future_cases_df['Case Case Start Date']=future_cases_df['Case Case Start Date'].dt.strftime('%Y-%m-%d')
#future_cases_df['Case Case Start Date']=future_cases_df['Case Case Start Date'].dt.strftime('%Y-%m-%d')
future_cases_df['Case Start Date']=future_cases_df['Case Start Date'].dt.strftime('%m/%d/%Y')
future_cases_df['Case End Date'] = pandas.to_datetime(future_cases_df['Case End Date']).dt.strftime('%m/%d/%Y')
future_cases_df['Last Modified Date']=pandas.to_datetime(future_cases_df['Last Modified Date']).dt.strftime('%m/%d/%Y')

open_cases_df['Case Start Date']=pandas.to_datetime(open_cases_df['Case Start Date']).dt.strftime('%m/%d/%Y')
open_cases_df['Case End Date']=pandas.to_datetime(open_cases_df['Case End Date']).dt.strftime('%m/%d/%Y')
open_cases_df['Last Modified Date']=pandas.to_datetime(open_cases_df['Case End Date']).dt.strftime('%m/%d/%Y')


open_denied_df['Case Start Date']=pandas.to_datetime(open_denied_df['Case Start Date']).dt.strftime('%m/%d/%Y')
open_denied_df['Case End Date']=pandas.to_datetime(open_denied_df['Case End Date']).dt.strftime('%m/%d/%Y')
open_denied_df['Last Modified Date']=pandas.to_datetime(open_denied_df['Case End Date']).dt.strftime('%m/%d/%Y')

closed_cases_df['Case Start Date']=pandas.to_datetime(closed_cases_df['Case Start Date']).dt.strftime('%m/%d/%Y')
closed_cases_df['Case End Date']=pandas.to_datetime(closed_cases_df['Case End Date']).dt.strftime('%m/%d/%Y')
closed_cases_df['Last Modified Date']=pandas.to_datetime(closed_cases_df['Case End Date']).dt.strftime('%m/%d/%Y')

writer = pandas.ExcelWriter("pandas_column_formats.xlsx", engine='xlsxwriter')# Set the column width and format. 
# Provide proper column where you have date info.
# Convert the dataframe to an XlsxWriter Excel object.
open_cases_df=open_cases_df.fillna('') # Fill NaN values with empty strings to avoid issues with Excel
print(open_cases_df['FMLA Exhaust Date'])
open_cases_df.to_excel(writer, sheet_name='Open Cases', index=False)
closed_cases_df=closed_cases_df.fillna('')
closed_cases_df.to_excel(writer, sheet_name='Closed Cases', index=False)
open_denied_df=open_denied_df.fillna('')
open_denied_df.to_excel(writer, sheet_name='Open-Denied', index=False)
future_cases_df=future_cases_df.fillna('')
future_cases_df.to_excel(writer, sheet_name='Future Cases', index=False)

workbook = writer.book
format = workbook.add_format({'num_format': 'mm/dd/yyyy'}) # Define the date format
for i in 'Open Cases', 'Closed Cases', 'Open-Denied', 'Future Cases':
  worksheet = writer.sheets[i]
  # Set the column width and format for date columns
  worksheet.set_column('D:D', 18, format)
  worksheet.set_column('E:E', 18, format)
  worksheet.set_column('K:K', 18, format)

writer.save()