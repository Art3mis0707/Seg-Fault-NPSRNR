import sqlite3 as sl
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
from PIL import Image, ImageTk
import mplcursors 



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
                #print(row)
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

    with con:
        con.executemany(sql_statement,row1)

        
def import_populationupdated_csv_into_database():
    
    con = sl.connect("COVID.db")

    with con:
            con.execute("""
                DROP table IF EXISTS updated_population_data;           
                """)
            con.execute("""
                CREATE TABLE IF NOT EXISTS updated_population_data (
                row_number INTEGER NOT NULL PRIMARY KEY,
                xLocation INTEGER,
                A INTEGER,
                B INTEGER,
                C INTEGER,
                D INTEGER,
                E INTEGER,
                F INTEGER,
                G INTEGER,
                H INTEGER,
                I INTEGER,
                J INTEGER,
                K INTEGER,
                L INTEGER,
                M INTEGER,
                N INTEGER,
                O INTEGER,
                P INTEGER,
                Q INTEGER,
                R INTEGER,
                S INTEGER,
                T INTEGER         
            );
        """)

    row1 = [[]]
    row1.clear()
    sql_statement = 'INSERT INTO updated_population_data values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'


    with open ("C:/Users/rahul/downloads/updated_covid.csv") as updated_population_file:
        csv_reader = csv.reader(updated_population_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                coords = str(row[0]) + "," + str(row[1])
                row.insert(0,line_count)
                row1.append(row)
                #print(row)
                line_count += 1

    #print(row1)
    
    with con:
        con.executemany(sql_statement,row1)



import_covid_csv_into_database()
import_population_csv_into_database()
import_populationupdated_csv_into_database()

con = sl.connect("COVID.db")

stat = "SELECT patient_id,TimeOfInfection,TimeOfReporting, patient_data.xLocation, patient_data.yLocation, Age,Diabetes,RespiratoryIllness, AbnormalBloodPressure, Outcome, Coordinates, population_data.Population FROM patient_data INNER JOIN population_data ON (patient_data.xLocation = population_data.xLocation) AND (patient_data.yLocation = population_data.yLocation)"
##join_table = con.execute(stat)

#pandas data frame can be used for plotting
combined_data_frame = pd.read_sql_query(stat, con)
population_data_frame = pd.read_sql_query("SELECT * from population_data", con)
updated_population_data_frame = pd.read_sql_query("SELECT * from updated_population_data", con)

con = sl.connect("COVID.db")


with con:

    def covid_conclusion():
   
        data = con.execute("SELECT * FROM patient_data WHERE ((Diabetes = 'True') OR (RespiratoryIllness = 'True')OR (RespiratoryIllness = 'True') OR (AbnormalBloodPressure ='True')) AND (Outcome = 'Alive')")
        print("number of ppl alive inspite of having diabetes,respillness,abnormalBP = ", len(data.fetchall()))
   

        data = con.execute("SELECT * FROM patient_data WHERE (Age < 50) AND (Outcome = 'Dead')")
        print("number of ppl who died below age of 50 = ", len(data.fetchall()))
    
        data = con.execute("SELECT * FROM patient_data WHERE ((Diabetes = 'False') AND (RespiratoryIllness = 'False') AND (RespiratoryIllness = 'False') AND (AbnormalBloodPressure ='False')) AND (Outcome = 'Dead')")
        print("number of ppl who died inspite of NOT having  diabetes,respillness,abnormalBP = ", len(data.fetchall()))
    
        data = con.execute("SELECT * FROM patient_data WHERE (Outcome = 'Dead')")
        print("Total number of dead people =" , len(data.fetchall()) )
       

 #Plotting
 #cases vs age
    
def pop_heat():
    
    # x = np.array(df['x location'])
    # y = np.array(df['y location'])
    x = np.arange(0, 20)
    y = np.arange(0, 20)
    heatmap = np.array(population_data_frame['Population']).reshape(20, 20)

    fig = plt.figure(figsize=(20,20))
    ax = plt.subplot()
    ax.imshow(heatmap)
    ax.set_xticks(x)
    ax.set_yticks(y)
    ax.set_xticklabels([str(i+1) for i in x], rotation=90)
    ax.set_yticklabels([str(i+1) for i in y])

    for a in range(len(np.arange(1, 21))):
        for b in range(len(np.arange(1, 21))):
            text = ax.text(a, b, heatmap[a, b], ha='center', va='center', color='w')
    plt.show()

    
def cases_heat():
    
    c = updated_population_data_frame.replace(to_replace= "", value=0)
    #x = c['xLocation']
    #y = c.columns[1:]
    x = np.arange(0, 20)
    y = np.arange(0, 20)
    fig = plt.figure(figsize=(20, 20))
    heat = c.values
    ax = plt.subplot()
    ax.imshow(heat)
    ax.set_xticks(range(0, 20))
    ax.set_yticks(range(0, 20))
    ax.set_xticklabels([str(i+1) for i in range(0, 20)], rotation=90)
    ax.set_yticklabels([str(i+1) for i in range(0, 20)])
    for a in range(len(np.arange(1, 21))):
        for b in range(len(np.arange(1, 21))):
            text = ax.text(a, b, heat[a, b], ha='center', va='center', color='w')
    plt.show()
    
    
def ages_cases():

    age = combined_data_frame[(combined_data_frame['Outcome'] == "Alive") | (combined_data_frame['Outcome'] == 'Dead')].groupby('Age')['TimeOfReporting'].count()

    fig = plt.figure(figsize=(10, 10))
    ax = plt.subplot()
    barz = ax.bar(range(0, 90), age, color='#33FF4C')
    plt.title('Cases per Age')
    plt.xlabel('Ages')
    plt.ylabel('Cases')
    ax.set_xticks(range(0, 90, 10))
    ax.set_yticks(range(0,10000,1000))
    ax.set_xticklabels([str(i) for i in range(0, 90, 10)], rotation=90)
    mplcursors.cursor(barz)
    plt.show()



#deaths vs age
def ages_deaths():

    deaths = combined_data_frame[combined_data_frame['Outcome'] == "Dead"].groupby('Age')['TimeOfReporting'].count()


    fig = plt.figure(figsize=(10, 10))
    ax = plt.subplot()

    barz = ax.bar(range(0, 90), deaths, color='#900C3F')
    plt.title('Deaths per Age')
    plt.xlabel('Ages')
    plt.ylabel('Deaths')
    ax.set_yticks(range(0, 250, 10))
    ax.set_xticks(range(0,90, 10))
    mplcursors.cursor(barz)

    plt.show()



#recovered vs age
def ages_recoveries():
    deaths = combined_data_frame[combined_data_frame['Outcome'] == "Alive"].groupby('Age')['TimeOfReporting'].count()


    fig = plt.figure(figsize=(10, 10))
    ax = plt.subplot()
    barz = ax.bar(range(0, 90), deaths, color='#FFC300')
    plt.title('Recoveries per Age')
    plt.xlabel('Ages')
    plt.ylabel('Recovered')
    ax.set_xticks(range(0,90, 10))
    mplcursors.cursor(barz)

    plt.show()
    
#Time of reporting vs count
def time_cases():

    time = combined_data_frame.groupby('TimeOfReporting')['xLocation'].count()
    fig = plt.figure(figsize=(10, 10))
    ax = plt.subplot()
    plt.plot(range(1, 246), time, color='#F001FF')
    plt.title('Cases Per Time')
    plt.xlabel('Time')
    plt.ylabel('Cases')
    ax.set_yticks(range(0, time.max(), 500))
    ax.set_xticks(range(0, 246, 10))
    plt.show()
    
    print('Time when cases were maximum: {}'.format(list(time).index(time.max())))
    print('Time when cases were minimum: {}'.format(list(time).index(time.min())))

#mortality rate vs ages
def mortality_rate():
    dead_per_age = combined_data_frame[combined_data_frame['Outcome'] == 'Dead'].groupby('Age')['Outcome'].count()
    ppl_per_age = combined_data_frame.groupby('Age')['Outcome'].count()

    mortality = (dead_per_age / ppl_per_age) * 100

    fig = plt.figure(figsize=(10, 10))
    ax = plt.subplot()
    plt.plot(range(0, 90), mortality, color='#1300FF', marker='o')
    ax.set_xticks(range(0, 90, 10))
    ax.set_yticks(np.arange(0, 10, 0.5))
    plt.xlabel('Ages')
    plt.ylabel('Mortality Rate')
    plt.title('Mortality Rate per Age')
    plt.show()

    print('Age group with highest mortality rate: {}'.format(list(mortality).index(mortality.max())))




root = Tk()


fr1 = Frame(root, bg='white')
fr1.place(relheight=1, relx=0.2, relwidth=0.8)

population = Button(fr1, text='Population Heatmap', bg='#00047B', fg='white', command=pop_heat)
population.place(relheight=1/3, relwidth=0.5)

cases = Button(fr1, text='Cases Heatmap', bg='#003E0E', fg='#00FF3A', command=cases_heat)
cases.place(relheight=1/3, relwidth=0.5, relx=0.5)

a_c = Button(fr1, text='Cases per Age', bg='red', fg='yellow', command=ages_cases)
a_c.place(relheight=1/3, relwidth=0.5, rely=1/3)

a_d = Button(fr1, text='Deaths per Age', bg='#581845', fg='#FF0083', command=ages_deaths)
a_d.place(relheight=1/3, relwidth=0.5, relx=0.5, rely=1/3)

a_r = Button(fr1, text='Recoveries per Age', bg='#00FFF0', fg='#838383', command=ages_recoveries)
a_r.place(relheight=1/3, relwidth=0.5, rely=2/3)

t_c = Button(fr1, text='Cases per Time', bg='#0FB275', fg='#DAF7A6', command=time_cases)
t_c.place(relheight=1/3, relwidth=0.5, relx=0.5, rely=2/3)


fr2 = Frame(root)
fr2.place(relheight=1, relwidth=0.2)

m_r = Button(fr2, text='Mortality Rate', bg='white', fg='black', command=mortality_rate)
m_r.place(relheight=1/3, relwidth=1, rely=2/3)

conc = Button(fr2, text='Conclusions', bg='#644613', fg='#F7E8A6', command=covid_conclusion)
conc.place(relheight=2/3, relwidth=1)

root.mainloop()
