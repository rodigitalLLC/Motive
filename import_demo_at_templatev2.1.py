import sys
import pandas

#  WPCU
#def country_xlate(s):
  # RTA-CM
  #if s =='ON':
    #return 'CA'
  #else:
    #return 'US'

#def work_location_xlate(w):
  #work_locations = {
  #"Location":"State Code"
  #}
  #return work_locations[w]

def set_manager_id(m,l):
  # query the dataframe using the manager last name, manager first name
  id=m['EmployeeID']
  rv=""

  try:
   q="`EmployeeID`=='"+id+"'"
  except Exception as e:
    print('Cant build query:')
    print(e)
    rv=""
  else:
    print(q)
    r=l.query(q)
    print("BOBO")
    print(r)
    try:
     rv=r['Last Name'].iloc[0]
    except Exception as e:
      print(e)
      rv=""
  
  print("Returning "+rv+"on "+id)
  #print(dir(rv))
  return rv



def set_hire_date(r):
  if r['ReHire Date'] !="":
    if r['ReHire Date']< r['Hire Date']:
      r['Hire Date']=r['ReHire Date']

  return r

def state_xlate(s):
  us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
    "Ontario":"ON"
  }
  return(us_state_to_abbrev[s.strip()])


def output_to_at_csv(df):
  template=[
    'Type', #A
    'EmployeeID', #B
    'Last Name', #C
    'First Name',#D
    'Middle Name', #E
    'Title', #F
    'Location', #G
    'Work State', #H
    'Work Country', #I
    'Home Phone', #J
    'Work Phone', #K
    'Mobile Phone', #L
    'Employee Phone Alt', #M
    'Business Email', #N
    'Personal Email', #O
    'Address',#P
    'Address Line 2',#Q
    'City', #R
    'State', #S
    'Zip', #T
    'Country',#U
    'PT/FT', #V
    'Manager Employee No', #W
    'Manager Last', #X
    'Manager First', #Y
    'Manager Phone', #Z
    'Manager Email', #AA
    'HR Contact Emp No', #AB
    'HR Contact Last', #AC
    'HR Contact First', #AD
    'HR Contact Phone', #AE
    'HR Contact Email', #AF
    'Spouse Emp No', #AG
    'DOB', #AH
    'Gender', #AI
    'Exempt-NonExempt', #AJ
    '50/75', #AK
    'Key Employee', #AL
    'Military Status',#AM
    'Employment Status',#AN
    'Term Date',#AO
    'Pay Rate',#AP
    'Pay Type',#AQ
    'Hire Date',#AR
    'ReHire Date',#AS
    'Service Date',#AT
    'Minutes Per Week',#AU
    'Hrs worked past 12 mos',#AV
    'Sunday',#AW
    'Monday',#AX
    'Tuesday',#AY
    'Wednesday',#AZ
    'Thursday',#BA
    'Friday',#BB
    'Saturday',#BC
    'Variable Flag', #BD
    'Effective Date',#BE 
    'Job Classification',#BF
    'Case Status',#BG
    'Cost Center',#BH
    'Schedule Effective Date',#BI
    'Employee Reference Code',#BJ
    'SSN',#BK
    'Pay Schedule',#BL
    'Start Date of Week',#BM
    'Average Weekly Minutes',#BN
    'Work County',#BO
    'Residence County',#BP
    'Work City',#BQ
    'Airline Flight Crew',#BQ
    ]
  df.to_csv('wpcu.csv',index=False,columns=template)

def rename_cols(df):
 return df.rename(columns={
    "EMPLOYEE NUMBER":"EmployeeID",
    "EMPLOYEE LAST NAME":"Last Name",
    "EMPLOYEE LEGAL FIRST NAME":"First Name",
    "EMPLOYEE MIDDLE NAME":"Middle Name",
    "Hours Worked":"Hrs worked past 12 mos",
    "DATE OF BIRTH":"DOB",
    "GENDER FOR INSURANCE":"Gender",
    "JOB TITLE":"Title",
    "DEPARTMENT":"Location",
    "COMPANY CODE":"Cost Center",
    "EXEMPT/NONEXEMPT STS":"Exempt-NonExempt",
    "HIRE DATE":"Hire Date",
    "EMPLOYEE PHONE HOME":"Home Phone",
    "EMPLOYEE PHONE WORK":"Work Phone",
    "EMPLOYEE PH MOBILE":"Mobile Phone",
    "EMPLOYEE WORK EMAIL":"Business Email",
    "EMPLOYEE PERSONAL EMAIL":"Personal Email",
    "MAILING ADDRESS":"Address",
    "MAILING ADDRESS 2":"Address Line 2",
    "MAILING CITY":"City",
    "MAILING STATE":"State",
    "MAILING POSTAL CODE":"Zip",
    "MAILING COUNTRY":"Country",
    "MANAGER WORK EMAIL":"Manager Email",
    "ADJ HIRE DATE":"ReHire Date",
    "TERM DATE":"Term Date",
    "WORKED IN STATE":"Work State",
    "MANAGER NUMBER":"Manager Employee No"
  })

# hire date could equal seniority date
def customize(xls,lookup):
  # need to split the name and csz
  xls['Type']='E'
  xls['Country']=xls['Country'].apply(lambda x: x[:2] if x=='USA' else x)
  xls['Work Country']=xls['Country']
  xls['Term Date']=pandas.to_datetime(xls['Term Date'])
  xls['ReHire Date']=pandas.to_datetime(xls['ReHire Date'])
  xls['Hire Date']=pandas.to_datetime(xls['Hire Date'])

  #xls['ReHire Date']=xls['ReHire Date'].apply(lambda x: '' if x=='' else x)
  #xls['ReHire Date']=xls['ReHire Date'].strftime('%m/%d/%y')
  xls['Employment Status']='A'
  xls['Employment Status']=xls['Term Date'].apply(lambda x: 'A' if x is pandas.NaT else 'T')
  #xls=xls.apply(set_hire_date, axis=1)
  #xls['Gender']=xls['Gender'].apply(lambda x: x[:1])
  xls['Gender']=xls['Gender'].apply(lambda x: 'U' if 'X' in x else x)
  xls['Exempt-NonExempt']=xls['Exempt-NonExempt'].apply(lambda x: x[:1])
  #xls['Exempt-NonExempt']=xls['Benefit Classification'].apply(lambda x: 'E' if "Salary" in x else 'N')
  #xls['Work State']=xls['Location'].apply(lambda x: x[x.find(',')+2:] if "," in x else 'CA')
  #xls.loc[:,'Work State']='OH' # Assumption
  # missing columns
  #xls['Business Email']=xls['Email Address']
  #xls.rename(columns={xls.columns[21]:"Gender"},inplace=True,errors="raise")
  xls['Service Date']=xls['Hire Date']
  #xls['State']=xls['State'].apply(lambda x:state_xlate(x))

  #xls['Country']=xls['State'].apply(lambda x:country_xlate(x))
  #xls['Work Country']=xls['Country']

    #xls=xls.assign(**{'Manager Last':'','Manager First':''})
  #xls['ReHire Date']=pandas.to_datetime(xls['ReHire Date'])
  #print(xls['ReHire Date'])
  #xls['ReHire Date']=xls['ReHire Date'].strftime('%m/%d/%y')
  #xls['ReHire Date']=xls['ReHire Date'].dt.strftime('%m/%d/%y')

  #xls['Work State']=xls['Location'].apply(lambda x:work_location_xlate(x))
  #xls['Work State']=xls['Location'].apply(lambda x:work_location_xlate(x))
  #xls['Work Country']=xls['Work State'].apply(lambda x:country_xlate(x))
  #xls['Home Phone']=xls['Home Phone'][:1].str.replace('-','')
  xls['Home Phone']=xls['Home Phone'].apply(lambda x: x.replace('-',''))
  xls['Mobile Phone']=xls['Mobile Phone'].apply(lambda x: x.replace('-',''))
  xls['Work Phone']=xls['Work Phone'].apply(lambda x: x.replace('-',''))
  #xls['Employee Phone Alt']=xls['Employee Phone Alt'].apply(lambda x: x.replace('-',''))
  #xls['ReHire Date'].replace("NaT","", inplace=True)
  # define to '' those elements that are not present
  xls = xls.assign(**{'Manager Phone': '', 
                    'Manager Email':'',
                    'PT/FT':'',
                    'HR Contact Emp No':'', 
                    'HR Contact Last':'',
                    'HR Contact First':'',
                    'HR Contact Phone':'', 
                    'HR Contact Email':'', 
                    'Employee Phone Alt':'',
                    'Spouse Emp No':'', 
                    'Manager First':'',
                    'Manager Last':'',
                    '50/75':'', 
                    'Key Employee':'', 
                    'Military Status':'', 
                    'Pay Type':'', 
                    'Minutes Per Week':'', 
                    'Sunday':'', 
                    'Monday':'480', 
                    'Tuesday':'480', 
                    'Wednesday':'480', 
                    'Thursday':'480', 
                    'Friday':'480', 
                    'Saturday':'',
                    'Variable Flag':'',
                    'Effective Date':'', 
                    'Case Status':'', 
                    'Schedule Effective Date':'', 
                    'SSN':'', 
                    'Pay Schedule':'', 
                    'Start Date of Week':'', 
                    'Average Weekly Minutes':'', 
                    'Work County':'', 
                    'Residence County':'', 
                    'Work City':'', 
                    'Pay Rate':'', 
                    'Job Classification':'',
                    'Employee Reference Code':'',
                    'Airline Flight Crew':'',
                    })
  

  #xls['Manager Employee No']=xls.apply(set_manager_id,l=lookup,axis=1)
  #xls['Manager Employee No']=xls.apply(set_manager_id,l=lookup,axis=1)
  xls['Home Phone']=xls['Home Phone'].apply(lambda x: '' if x=='0' else x)
  xls['Mobile Phone']=xls['Mobile Phone'].apply(lambda x: '' if x=='0' else x)
  xls['Work Phone']=xls['Work Phone'].apply(lambda x: '' if x=='0' else x)
  #xls['Employee Phone Alt']=xls['Employee Phone Alt'].apply(lambda x: '' if x=='0' else x)

  xls['Home Phone']=xls['Home Phone'].apply(lambda x: '{ignore}' if x=='' else x)
  xls['Mobile Phone']=xls['Mobile Phone'].apply(lambda x: '{ignore}' if x=='' else x)
  xls['Work Phone']=xls['Work Phone'].apply(lambda x: '{ignore}' if x=='' else x)
  #xls['Employee Phone Alt']=xls['Employee Phone Alt'].apply(lambda x: '{ignore}' if x=='' else x)
  return xls
# main

# database

# required columns: Type,EmployeeID,Last Name,First Name,Title,Work State,PT/FT,DOB,Gender,Exemption Status,Employment Status,Hire Date,Service Date
#if len(sys.argv)!=3:
  #print ("Usage: {} {} {}".format(sys.argv[0],"<input xlsx sheet>"))
  #sys.exit()

xl=pandas.read_csv(sys.argv[1],na_filter=False)
xls=xl.astype(str)

xl2=pandas.read_csv(sys.argv[2],na_filter=False)
xls2=xl2.astype(str)
#create new dataframe to join files
print(xls)
print(xls2)
#xls=xls.set_index('EMPLOYEE NUMBER').join(xls2.set_index('EMPLOYEE NUMBER'),rsuffix="2")
xls=pandas.merge(xls,xls2,on="EMPLOYEE NUMBER")
#print(xls)
# 
# debug out
xls.to_csv('debug.csv')
xls=rename_cols(xls)
# create a lookup table of id,last,first
#print(xls)
#for i in xls.columns:
  #print(i)

#xls.to_csv('debug.csv')
print(xls)
lookup=xls[['EmployeeID']]
xls=customize(xls,lookup)
#print(xls)
output_to_at_csv(xls)