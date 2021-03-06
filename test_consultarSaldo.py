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

class TestSaldo(TestCase):
    def testSaldoCorrecto(self):
        try:
            print("********** Unit Test - Consultar Saldo")
            noCuenta = 1000000

            # valida que los campos esten declarados
            if noCuenta:
                # All Good, let's call MySQL
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.callproc('sp_saldo', (int(noCuenta),))
                data = cursor.fetchall()
                conn.commit()
                for row in data:
                    saldo = str(row[0])

                print("Exito! Su Saldo: "+saldo)

            else:
                return json.dumps({'html': '<span>Enter the required fields</span>'})

        except Exception as e:
            print("ERROR")


    def testSaldoIncorrecto(self):
        try:
            noCuenta = 10000

            # valida que los campos esten declarados
            if noCuenta:
                # All Good, let's call MySQL
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.callproc('sp_saldo', (int(noCuenta),))
                data = cursor.fetchall()
                conn.commit()
                for row in data:
                    saldo = str(row[0])
                print("Saldo: "+str(saldo))

            else:
                return json.dumps({'html': '<span>Enter the required fields</span>'})

        except Exception as e:
            print("ERROR en obtener el saldo, no se encontro el numero de cuenta")
            print("------------------------------")

if __name__ == '__main__':
    unittest.main()
