import sqlite3
# Connectt to SQlite
connection=sqlite3.connect("library.db")

# Create a cursor object to insert record,create table

cursor=connection.cursor()

## create the table
table_info="""
create table publisher (
pname varchar(10) primary key,
address varchar(10),
phone varchar(10)
);"""

table_info2="""
create table book(
bookid int primary key,
title varchar(10),
pname references publisher(pname),
pub_year int
);"""

table_info3="""
create table book_author(
author_name varchar(10) primary key,
bookid references book(bookid) on delete cascade
);"""

table_info4="""
create table libprogram(
prgid int primary key,
prgname varchar(10),
prgaddress varchar(10)
);"""
table_info5="""
create table book_copies(
bookid references book(bookid) on delete cascade,
prgid references libprogram(prgid) on delete cascade,
No_of_Copies int
);"""

table_info6="""
create table card(
card_no int primary key);"""

table_info7="""
create table book_lending(
bookid references book(bookid) on delete cascade,
prgid references libprogram(prgid) on delete cascade,
card_no references card(card_no) on delete cascade,
date_out date,
due_date date
);"""



cursor.execute(table_info)
cursor.execute(table_info2)
cursor.execute(table_info3)
cursor.execute(table_info4)
cursor.execute(table_info5)
cursor.execute(table_info6)
cursor.execute(table_info7)

## Insert Some more records

cursor.execute('''insert into publisher values('Raka','mp',12345)''');
cursor.execute('''insert into publisher values('swati','hp',6789);''')
cursor.execute('''insert into publisher values('haka','jk',9876);''')
cursor.execute('''insert into publisher values('dhaka','up',4567)''');
cursor.execute('''insert into publisher values('saka','gk',7320);''')
cursor.execute('''insert into book values(1,'VIDEOEDIT','Raka',2002)''');
cursor.execute('''insert into book values(2,'filming','kaka',2001)''');
cursor.execute('''insert into book values(3,'editing','haka',2003)''');
cursor.execute('''insert into book values(4,'discipline','dhaka',2004)''');
cursor.execute('''insert into book values(5,'procast','saka',2005)''');

cursor.execute('''insert into book_author values('Sharma',1)''');
cursor.execute('''insert into book_author values('teja',2)''');
cursor.execute('''insert into book_author values('tri',3)''');
cursor.execute('''insert into book_author values('paliwal',4)''');
cursor.execute('''insert into book_author values('tyagi',5)''');

cursor.execute('''insert into libprogram values(1,'first','cse')''');
cursor.execute('''insert into libprogram values(2,'second','ise')''');
cursor.execute('''insert into libprogram values(3,'third','ece')''');
cursor.execute('''insert into libprogram values(4,'fourth','ete')''');
cursor.execute('''insert into libprogram values(5,'fifth','civil')''');

cursor.execute('''insert into book_copies values(1,1,3)''');
cursor.execute('''insert into book_copies values(2,2,8)''');
cursor.execute('''insert into book_copies values(3,3,7)''');
cursor.execute('''insert into book_copies values(4,4,9)''');
cursor.execute('''insert into book_copies values(5,5,2)''');

cursor.execute('''insert into card values(1)''');
cursor.execute('''insert into card values(2)''');
cursor.execute('''insert into card values(3)''');
cursor.execute('''insert into card values(4)''');
cursor.execute('''insert into card values(5)''');

cursor.execute('''insert into book_lending values(1,1,1,'01-jan-2021','02-jan-2023')''');
cursor.execute('''insert into book_lending values(2,2,2,'01-feb-2021','02-feb-2022')''');
cursor.execute('''insert into book_lending values(3,3,3,'01-apr-2021','02-apr-2021')''');
cursor.execute('''insert into book_lending values(4,4,4,'01-mar-2021','02-mar-2024')''');
cursor.execute('''insert into book_lending values(5,5,5,'01-june-2021','02-june-2023')''');

## Dispaly All the records

print("The inserted records are")
data=cursor.execute('''Select * from book_lending''')
for row in data:
    print(row)

## Commit your changes int he database
connection.commit()
connection.close()