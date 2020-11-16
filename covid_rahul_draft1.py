import sqlite3 as sl
import csv

    
con = sl.connect("COVID.db")
#
with con:
        #dropping the table created from previous run
        con.execute("""
            DROP table patient_data;           
            """)
        #creating a new database table with the given columns
        con.execute("""
            CREATE TABLE IF NOT EXISTS patient_data (
            patient_id INTEGER NOT NULL PRIMARY KEY,
            TimeOfInfection INTEGER,
            TimeOfReporting INTEGER,
            xLocation INTEGER,
            yLocation INTEGER,
            Age INTEGER,
            Diabetes TEXT,
            RespiratoryIllness TEXT,
            AbnormalBloodPressure TEXT,
            Outcome TEXT
        );
    """)
        

#using '?' as place holder
sql_statement = 'INSERT INTO patient_data values(?,?,?,?,?,?,?,?,?,?)'

with open ("C:/Users/rahul/downloads/COVID_Dataset.csv") as covid_file:
    csv_reader = csv.reader(covid_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        #Have tested only for 100 rows
        if line_count > 100:
            break
        if line_count == 0:
            #skipping the header
            line_count = line_count + 1
        else:
            line_count = line_count + 1
            #inserting a patient id as a primary key
            row.insert(0,line_count)
            #insert a row into database table
            with con:
                con.execute(sql_statement,row)


#sql_statement = 'INSERT INTO patient_data (TimeOfInfection, TimeOfReporting, xLocation, yLocation, Age, Diabetes, RespiratoryIllness, AbnormalBloodPressure, Outcome) values(?,?,?,?,?,?,?,?,?,?)'

#conclusions drawn so far    
with con:
    data = con.execute("SELECT * FROM patient_data WHERE ((Diabetes = 'True') OR (RespiratoryIllness = 'True')OR (RespiratoryIllness = 'True') OR (AbnormalBloodPressure ='True')) AND (Outcome = 'Alive')")
    print("num ppl alive inspite of having diabetes,respillness,abnormalBP = ", len(data.fetchall()))
   

    data = con.execute("SELECT * FROM patient_data WHERE (Age < 50) AND (Outcome = 'Dead')")
    print("num ppl who died below age of 50 = ", len(data.fetchall()))
    
    data = con.execute("SELECT * FROM patient_data WHERE ((Diabetes = 'False') AND (RespiratoryIllness = 'False') AND (RespiratoryIllness = 'False') AND (AbnormalBloodPressure ='False')) AND (Outcome = 'Dead')")
    print("num ppl who died inspite of having no diabetes,respillness,abnormalBP = ", len(data.fetchall()))
