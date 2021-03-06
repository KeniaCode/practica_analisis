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


class TestTransferencias(TestCase):
    def testTransfCorrecta(self):
        cuentaLog = '1000001'
        userLog = 'kcj'

        noCuenta = '1000000'
        montoPago = '0'

        try:
            if noCuenta and montoPago:
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.callproc('sp_transferencia', (int(cuentaLog), float(montoPago), int(noCuenta)))
                conn.commit()
                print ("transferencia exitosa")

        except Exception as e:
            print("ERROR en la transferencia")

    def testTransfInCorrecta(self):
        cuentaLog = '1'
        userLog = 'kcj'

        noCuenta = '2'
        montoPago = '0'

        try:
            if noCuenta and montoPago:
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.callproc('sp_transferencia', (int(cuentaLog), float(montoPago), int(noCuenta)))
                conn.commit()
                print ("transferencia exitosa")

        except Exception as e:
            print("ERROR en la transferencia - No se encontro cuenta destino")


if __name__ == '__main__':
    unittest.main()
