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


class TestLogin(TestCase):
    def testLogCorrecto(self):
        # Create Flask test client
        codigoI = '5fafqe'
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
            print ("usuario incorrecto")
        else:
            print ("usuario correcto")

    def testLogInCorrecto(self):
        # Create Flask test client
        codigoI = '2'
        usuario = 'kcj'
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

if __name__ == '__main__':
    unittest.main()