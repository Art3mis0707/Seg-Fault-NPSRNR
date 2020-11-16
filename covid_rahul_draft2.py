import sqlite3 as sl
import csv
import numpy as np
import pandas as pd



def import_covid_csv_into_database():
    
    con = sl.connect("COVID.db")

    with con:
        #dropping the table created from previous run
            con.execute("""
                DROP table IF EXISTS patient_data;           
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
    #creating a 2 dimenional array of lists
    row1 = [[]]
    row1.clear()
    #using '?' as place holder
    sql_statement = 'INSERT INTO patient_data values(?,?,?,?,?,?,?,?,?,?)'


    with open ("C:/Users/rahul/downloads/COVID_Dataset.csv") as covid_file:
        csv_reader = csv.reader(covid_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
             #skipping the header
                line_count += 1
            else:
                #inserting a patient id as a primary key
                row.insert(0,line_count)
                #adding a row to the array list
                row1.append(row)
                line_count += 1

    #print(row1)
    ##inserting all rows into the database table
    with con:
        con.executemany(sql_statement,row1)


        
#function to import population.csv into database
def import_population_csv_into_database():
    
    con = sl.connect("COVID.db")

    with con:
            con.execute("""
                DROP table IF EXISTS population_data;           
                """)
            con.execute("""
                CREATE TABLE IF NOT EXISTS population_data (
                row_number INTEGER NOT NULL PRIMARY KEY,
                xLocation INTEGER,
                yLocation INTEGER,
                Population INTEGER,
                Coordinates TEXT
               
            );
        """)

    row1 = [[]]
    row1.clear()
    sql_statement = 'INSERT INTO population_data values(?,?,?,?,?)'


    with open ("C:/Users/rahul/downloads/Population.csv") as Population_file:
        csv_reader = csv.reader(Population_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                coords = str(row[0]) + "," + str(row[1])
                row.insert(0,line_count)
                row.append(coords)
                row1.append(row)
                line_count += 1

    ##print(row1)
    
    with con:
        con.executemany(sql_statement,row1)



import_covid_csv_into_database()
import_population_csv_into_database()

con = sl.connect("COVID.db")

stat = "SELECT patient_id,TimeOfInfection,TimeOfReporting, patient_data.xLocation, patient_data.yLocation, Age,Diabetes,RespiratoryIllness, AbnormalBloodPressure, Outcome, Coordinates, population_data.Population FROM patient_data INNER JOIN population_data ON (patient_data.xLocation = population_data.xLocation) AND (patient_data.yLocation = population_data.yLocation)"
##join_table = con.execute(stat)

#pandas data frame can be used for plotting
combined_data_frame = pd.read_sql_query(stat, con)

##fig = px.line(combined_data_frame, x = 'Age', y = 'Outcome', title='Age vs Outcome')
##fig.show()

con = sl.connect("COVID.db")


with con:
    data = con.execute("SELECT * FROM patient_data WHERE ((Diabetes = 'True') OR (RespiratoryIllness = 'True')OR (RespiratoryIllness = 'True') OR (AbnormalBloodPressure ='True')) AND (Outcome = 'Alive')")
    print("number of ppl alive inspite of having diabetes,respillness,abnormalBP = ", len(data.fetchall()))
   

    data = con.execute("SELECT * FROM patient_data WHERE (Age < 50) AND (Outcome = 'Dead')")
    print("number of ppl who died below age of 50 = ", len(data.fetchall()))
    
    data = con.execute("SELECT * FROM patient_data WHERE ((Diabetes = 'False') AND (RespiratoryIllness = 'False') AND (RespiratoryIllness = 'False') AND (AbnormalBloodPressure ='False')) AND (Outcome = 'Dead')")
    print("number of ppl who died inspite of NOT having  diabetes,respillness,abnormalBP = ", len(data.fetchall()))
    
    data = con.execute("SELECT * FROM patient_data WHERE (Outcome = 'Dead')")
    print("Total number of dead people =" , len(data.fetchall()) )

    
    
