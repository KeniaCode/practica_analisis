import unittest
from unittest import TestCase
from flask import Flask
from flask import json
from flask_restful import Api
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'mynewpassword'
app.config['MYSQL_DATABASE_DB'] = 'mydb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
api = Api(app)


class TestLogin(TestCase):
    def testLogCorrecto(self):
        # Create Flask test client
        print ("-----------Test Login Correcto-------------")
        codigoI = '1'
        usuario = 'test'
        contrasenia = 'test23'
        if usuario and contrasenia:
            # All Good, let's call MySQL
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_login', (codigoI, usuario, contrasenia))
            data = cursor.fetchall()
            conn.commit()
        if len(data) is 0:
            print ("Login incorrecto")
        else:
            print ("Login correcto")

    def testLogInCorrectoUsuario(self):
        # Create Flask test client
        print ("-----------Test Login Usuario Incorrecto-------------")
        codigoI = '2'
        usuario = 'kcj1'
        contrasenia = 'kcj'
        if usuario and contrasenia:
            # All Good, let's call MySQL
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_login', (codigoI, usuario, contrasenia))
            data = cursor.fetchall()
            conn.commit()
        if len(data) is 0:
            print ("usuario incorrecto")
        else:
            print ("usuario correcto")


    def testLogInCorrectoContrasena(self):
        # Create Flask test client
        print ("-----------Test Login Contrasena Incorrecta-------------")
        codigoI = '2'
        usuario = 'kcj'
        contrasenia = 'kcjdasds1'
        if usuario and contrasenia:
            # All Good, let's call MySQL
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_login', (codigoI, usuario, contrasenia))
            data = cursor.fetchall()
            conn.commit()
        if len(data) is 0:
            print ("contrasena incorrecta")
        else:
            print ("constrasena incorrecta")

    def testLogInCorrectoCodigo(self):
        # Create Flask test client
        print ("-----------Test Login Codigo Incorrecto-------------")
        codigoI = '111111'
        usuario = 'kcj1'
        contrasenia = 'kcj'
        if usuario and contrasenia:
            # All Good, let's call MySQL
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_login', (codigoI, usuario, contrasenia))
            data = cursor.fetchall()
            conn.commit()
        if len(data) is 0:
            print ("codigo incorrecto")
        else:
            print ("codigo correcto")



if __name__ == '__main__':
    unittest.main()

