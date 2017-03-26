import unittest
from unittest import TestCase
from practica2AyD import app
from flask_restful import Api
from flaskext.mysql import MySQL

mysql = MySQL()

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
            noCuenta = 1000006
            montoPago = 25
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
            print("ERROR")
            return json.dumps({'error': str(e)})


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
            print("ERROR")
            return json.dumps({'error': str(e)})

if __name__ == '__main__':
    unittest.main()