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


class TestDebito(TestCase):
    def testDebitoCorrecto(self):
        print("********************** Unit Test - Debito")
        cuentaLog = '1000000'
        userLog = 'kcj'

        try:
            noCuenta = '1000001'
            montoPago = '0'
            descripcion = 'prueba unitaria de sp debito'

            if noCuenta and montoPago:
                # All Good, let's call MySQL
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.callproc('sp_debito', (int(cuentaLog), float(montoPago), int(noCuenta), descripcion))
                conn.commit()
                print ("Test Debito exitoso")

        except Exception as e:
            print("debito invalido")


    def testDebitoInCorrecto(self):
        cuentaLog = '1'
        userLog = 'kcj'

        try:
            noCuenta = '10000021'
            montoPago = '0'
            descripcion = 'prueba unitaria de sp debito'

            if noCuenta and montoPago:
                # All Good, let's call MySQL
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.callproc('sp_debito', (int(cuentaLog), float(montoPago), int(noCuenta), descripcion))
                conn.commit()
                print ("debito exitoso")

        except Exception as e:
            print("Error - Debito invalido - no se encuentra numero de cuenta destino")
            
            
            
    def testDebitoInPago(self):
        cuentaLog = '1'
        userLog = 'kcj'

        try:
            noCuenta = '10000001'
            montoPago = '1110000'
            descripcion = 'prueba unitaria de sp debito'

            if noCuenta and montoPago:
                # All Good, let's call MySQL
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.callproc('sp_debito', (int(cuentaLog), float(montoPago), int(noCuenta), descripcion))
                conn.commit()
                print ("debito exitoso")

        except Exception as e:
            print("Error - Debito invalido - No tiene suficiente capital")


if __name__ == '__main__':
    unittest.main()
