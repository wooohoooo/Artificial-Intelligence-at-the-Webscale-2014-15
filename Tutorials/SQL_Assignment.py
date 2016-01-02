import MySQLdb as mdb
import pandas as pd
import numpy as np

#connect to database
con = mdb.connect('localhost','testuser','test623','testdb');

##################create names database
with con:
	cur = con.cursor()
	cur.execute("DROP TABLE IF EXISTS Student_Names")
	cur.execute("CREATE TABLE Student_Names(id INT AUTO_INCREMENT,name VARCHAR(30),age INT,major VARCHAR(30),PRIMARY KEY(id))")
	name_list = ['Adam','Eve','Lucy','Kalliope','Danae','Ikarus','Antiope','Julius','Hank','Caren']
	major_list = ['theology','Ancient Greek','Latin','Pseudoscience','physics']*2



#fill database with name, age, major from lists
	for name,age,major in zip(name_list,np.random.random_integers(19,25,10),major_list):
			text = "INSERT INTO Student_Names(name,age,major) Values('"+name+"','"+ str(age)+"','"+major + "')"
			cur.execute(text)



#create grade database
	cur.execute("DROP TABLE IF EXISTS Student_Grades")
	cur.execute("CREATE TABLE Student_Grades(id INT AUTO_INCREMENT,name VARCHAR(30),grade INT,PRIMARY KEY(id))")
	ext_name_list = name_list*5



#fill database with name and grade
	for name,grade in zip(ext_name_list,np.random.random_integers(0,10,50)):
			text = "INSERT INTO Student_Grades(name,grade) Values('"+name+"','"+ str(grade)+"')"
			#print(text)
			cur.execute(text)
	cur.execute("SELECT AVG(grade) FROM Student_Grades")


###################'GET MEAN AND STD IN SEVERAL WAYS

df_names = pd.read_sql("SELECT * FROM Student_Names", con)
df_grades = pd.read_sql("SELECT * FROM Student_Grades",con)
df_mean = pd.read_sql("SELECT AVG(grade) FROM Student_Grades",con)
df_std = pd.read_sql("SELECT STD(grade) FROM Student_Grades",con)

print(df_names)
print(df_grades)
print('SQL AVG(), STD(): ')

print(df_mean)
print(df_std)
print('Utilizing Pandas for the mean and STD: ')
print(df_grades.grade.mean())
print(df_grades.grade.std())

#read in the names from the database
name_list = list(pd.read_sql("SELECT name FROM Student_Names",con).name)
print('names')
print(name_list)
for name in name_list:
#select via for loop
	df_mean_pp = pd.read_sql("SELECT AVG(grade) FROM Student_Grades WHERE name = '"+name+"'",con)
	df_std_pp = pd.read_sql("SELECT STD(grade) FROM Student_Grades WHERE name = '"+name+"'",con)
	print(name)
	print(df_mean_pp,df_std_pp)

#seletct without for loop with GROUPBY
df_mean_pp = pd.read_sql("SELECT n.name,AVG(g.grade) FROM Student_Names n, Student_Grades g WHERE n.name = g.name GROUP BY n.name",con)
print(df_mean_pp)








