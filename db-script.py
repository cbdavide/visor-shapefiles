#! /usr/bin/env python3

import sys
from PyQt5 import QtSql

db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
db.setDatabaseName('app.db')

if not db.open():
    print("Couldn't open the database.")
    sys.exit(1)

query = QtSql.QSqlQuery()

r = query.exec_("CREATE TABLE users(email varchar(50) primary key, "
    " password varchar(50))")

if not r:
    print("Couldn't create the table, perhaps it has been alraedy created.")
    sys.exit(1)
else:
    print('The table users has been successfully created.')

r = query.exec_("INSERT INTO users values('cbdavides@gmail.com', 'david950421')")
if not r:
    print("Couldn't insert the user into the table, "
           "perhaps the user has been already inserted.")
    sys.exit(1)
else:
    print('The user has been successfully inserted.')

db.close()
sys.exit(0)
