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



class TestPagoServicios(TestCase):
    def testPagoCorrecto(self):
        try:
            cuentaIngresado= 1000000
            tipo = 'Agua'
            noCuenta = 1000001
            montoPago = 0
            # valida que los campos esten declarados
            if noCuenta and montoPago:
                # All Good, let's call MySQL
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.callproc('sp_pago_servicios', (int(cuentaIngresado), float(montoPago), int(noCuenta), tipo))
                conn.commit()
                print("Exito - Pago realizado correctamente")


            else:
                print("ERROR - No se tipo de servicio")

        except Exception as e:
            print("ERROR")
            print("ERROR - No se tipo de servicio")


    def testPagoIncorrecto(self):
        try:
            cuentaIngresado = 10000000
            tipo = 'Agua'
            noCuenta = 100
            montoPago = 0
            # valida que los campos esten declarados
            if noCuenta and montoPago:
                # All Good, let's call MySQL
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.callproc('sp_pago_servicios', (int(cuentaIngresado), float(montoPago), int(noCuenta), tipo))
                conn.commit()
                print("Correcto")


            else:
                return json.dumps({'html': '<span>Enter the required fields</span>'})

        except Exception as e:
            print("ERROR - No  se encontro cuenta destino")
            print("ERROR - No se tipo de servicio")
        
        
    def testPagoInPago(self):
        try:
            cuentaIngresado = 10000000
            tipo = 'Agua'
            noCuenta = 1000002
            montoPago = 0
            # valida que los campos esten declarados
            if noCuenta and montoPago:
                # All Good, let's call MySQL
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.callproc('sp_pago_servicios', (int(cuentaIngresado), float(montoPago), int(noCuenta), tipo))
                conn.commit()
                print("Correcto")


            else:
                print("ERROR - No se tipo de servicio")

        except Exception as e:
            print("ERROR - No se encontro tipo de servicio")
            

if __name__ == '__main__':
    unittest.main()
