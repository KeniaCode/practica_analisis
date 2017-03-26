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



class TestCredito(TestCase):
    def testCreditoCorrecto(self):
        cuentaLog = '1000001'
        userLog = 'kcj'

        try:
            noCuenta = '1000045'
            montoPago = '400'
            descripcion = 'prueba unitaria de sp credito'

            if noCuenta and montoPago:
                # All Good, let's call MySQL
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.callproc('sp_credito', (int(cuentaLog), float(montoPago), int(noCuenta), descripcion))
                conn.commit()
                print ("credito exitoso")

        except Exception as e:
            print("credito invalido")


    def testCreditoInCorrecto(self):
        cuentaLog = '1'
        userLog = 'kcj'

        try:
            noCuenta = '10000021'
            montoPago = '0'
            descripcion = 'prueba unitaria de sp credito'

            if noCuenta and montoPago:
                # All Good, let's call MySQL
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.callproc('sp_credito', (int(cuentaLog), float(montoPago), int(noCuenta), descripcion))
                conn.commit()
                print ("credito exitoso")

        except Exception as e:
            print("credito invalido")

if __name__ == '__main__':
    unittest.main()