# -*- coding: utf-8 -*-

import sys
from PyQt4.QtSql import QSqlDatabase, QSqlQuery

class Model:
    def __init__(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('app.db')

        if not db.open():
            print("Couldn't open the database.")
            sys.exit(1)

    def checkUser(self, email, password):
        query = QSqlQuery()
        query_str = "SELECT * FROM users WHERE email='{}' AND password='{}'"
        query.exec_(query_str.format(email, password))

        return query.first()

if __name__ == '__main__':
    model = Model()
    r = model.checkUser('cbdavides@gmail.com', 'david950421')
    assert r
    r = model.checkUser('unregistered@gmail.com', 'abc')
    assert not r
