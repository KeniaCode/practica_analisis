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

class TestRegistro(TestCase):
    def testRegCorrecto(self):
        # Create Flask test client
        usuarioN = 'pepito2'
        nombreU = 'pepe2'
        passU = 'pepe2'
        emailU = 'pepe2@gmail.com'
        # valida que los campos esten declarados
        if usuarioN and passU:
            # All Good, let's call MySQL
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_registro', (usuarioN, passU, nombreU, emailU))
            data = cursor.fetchall()
            conn.commit()
            # el procedimiento de sql retorno que no se contro al usuario
            if len(data) is 0:
                print("registro FALLIDO")
            else:
                print("registro EXISTO")
                for row in data:
                    codigox = str(row[0])
                    print ("codigo: " + codigox)




    def testRegIncorrecto(self):
        # Create Flask test client
        usuarioN = 'kenia'
        nombreU = 'kenia'
        passU = '123456'
        emailU = 'kenia@gmail.com'
        # valida que los campos esten declarados
        if usuarioN and passU:
            # All Good, let's call MySQL
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_registro', (usuarioN, passU, nombreU, emailU))
            data = cursor.fetchall()
            conn.commit()
            # el procedimiento de sql retorno que no se contro al usuario
            if len(data) is 0:
                print("registro FALLIDO")
            else:
                print("registro EXITOSO")

if __name__ == '__main__':
    unittest.main()