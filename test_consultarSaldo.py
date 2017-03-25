import unittest
from unittest import TestCase
import practica2AyD
from practica2AyD import login

from practica2AyD import app

from flask import Flask, render_template, redirect, url_for, request, jsonify, json, flash
from flask_restful import Resource, Api
from flask_restful import reqparse
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
            noCuenta = 1000045

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

                print("Saldo: "+saldo)

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
            print("ERROR")



if __name__ == '__main__':
    unittest.main()