from flask import Flask, render_template, redirect, url_for, request, jsonify, json, flash
from flask_restful import Resource, Api
from flask_restful import reqparse
from flaskext.mysql import MySQL



# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'mynewpassword'
app.config['MYSQL_DATABASE_DB'] = 'mydb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
api = Api(app)


#aqui vamos a guardar el usuario y su codigo
userIngresado = ''
codigoIngresado = ''



@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    usuarioexist = False
    global userIngresado
    global codigoIngresado
    global cuentaIngresado

    # en los htmls se declara un metodo post que se dispara cuando precionan el boton de login
    if request.method == 'POST':
        codigoI = request.form['cod']
        usuario = request.form['user']
        contrasenia = request.form['pass']
        # valida que los campos esten declarados
        if usuario and contrasenia:
            # All Good, let's call MySQL
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_login', (codigoI, usuario, contrasenia))
            data = cursor.fetchall()
            conn.commit()
            for row in data:
                print str(row[2])

            # el procedimiento de sql retorno que no se contro al usuario
            if len(data) is 0:
                print("usuario incorrecto")
                flash('Usuario o contrasenia incorrectos')
                return json.dumps({'message': 'Usuario incorrecto !'})
            else:
                flash('Logueado')

                for row in data:
                    cuentaIngresado = str(row[2])


                # en teoria se encontro el usuario entonces vamos a ingresar a su cuenta
                userIngresado = usuario
                # estas las vamos a usar como para guardar las variables de sesion globales
                codigoIngresado = codigoI

                return redirect(url_for('ingresado'))

        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})

    return render_template('login.html', error=error)


# *********************************************************registrarse*******************


@app.route('/Registrar', methods=['POST', 'GET'])
def registrarse():
    error = None
    usuarioexist = False

    # en los htmls se declara un metodo post que se dispara cuando precionan el boton de login
    if request.method == 'POST':
        try:
            usuarioN = request.form['user']
            nombreU = request.form['name']
            passU = request.form['pass']
            emailU = request.form['email']
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
                        print ("codigo: " +codigox)
                        flash(codigox)

            else:
                return json.dumps({'html': '<span>Enter the required fields</span>'})


        except Exception as e:
            return json.dumps({'error': str(e)})
        finally:
            cursor.close()
            conn.close()
            return redirect(url_for('login'))

    return render_template('registrarse.html')


# *********************************************************************************************
@app.route('/testing')
def testing():
    return 'user: '+userIngresado


# **********************************************

@app.route('/reportesMenu', methods=['GET', 'POST'])
def reportesMenu():
    return render_template('reportesTable.html')


# ****************************************************************

@app.route('/ingresado')
def ingresado():
    return render_template('ingresado.html')

@app.route('/pagoServicios', methods=['POST', 'GET'])
def pagoServicios():
    l = []
    l.append("Agua")
    l.append("Telefono")
    l.append("Luz")
    l.append("Colegio")

    ctx = {"l": l}
    cuentaLog = cuentaIngresado
    userLog = userIngresado

    # en los htmls se declara un metodo post que se dispara cuando precionan el boton de login
    if request.method == 'POST':
        try:
            tipo = request.form['idCombo']
            noCuenta = request.form['noCuenta']
            montoPago = request.form['montoPago']
            # valida que los campos esten declarados
            if noCuenta and montoPago:
                # All Good, let's call MySQL
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.callproc('sp_pago_servicios', (int(cuentaIngresado), float(montoPago), int(noCuenta), tipo))
                conn.commit()

            else:
                return json.dumps({'html': '<span>Enter the required fields</span>'})

        except Exception as e:
            print("ERROR")
            return json.dumps({'error': str(e)})

        finally:
            cursor.close()
            conn.close()

    return render_template('pagoServicios.html',  l=l, cuentaLog=cuentaLog, userLog=userLog)



@app.route('/transferencias', methods=['POST', 'GET'])
def transferencias():

    cuentaLog = cuentaIngresado
    userLog = userIngresado

    # en los htmls se declara un metodo post que se dispara cuando precionan el boton de login
    if request.method == 'POST':
        try:
            noCuenta = request.form['noCuenta']
            montoPago = request.form['monto']
            # valida que los campos esten declarados
            if noCuenta and montoPago:
                # All Good, let's call MySQL
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.callproc('sp_transferencia', (int(cuentaIngresado), float(montoPago), int(noCuenta)))
                conn.commit()
                #  data = cursor.fetchall()

            else:
                return json.dumps({'html': '<span>Enter the required fields</span>'})

        except Exception as e:
            print("ERROR")
            return json.dumps({'error': str(e)})

        finally:
            cursor.close()
            conn.close()

    return render_template('transferencias.html',cuentaLog=cuentaLog, userLog=userLog)

@app.route('/consultarSaldo', methods=['POST', 'GET'])
def consultarSaldo():

    cuentaLog = cuentaIngresado
    userLog = userIngresado
    saldo = 0

    # en los htmls se declara un metodo post que se dispara cuando precionan el boton de login
    if request.method == 'POST':
        try:
            noCuenta = request.form['noCuenta']

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
                    print(str(saldo))

            else:
                return json.dumps({'html': '<span>Enter the required fields</span>'})

        except Exception as e:
            print("ERROR")
            return json.dumps({'error': str(e)})

    return render_template('consultarSaldo.html',cuentaLog=cuentaLog, userLog=userLog, saldo=saldo)

@app.route('/credito', methods=['POST', 'GET'])
def credito():

    cuentaLog = cuentaIngresado
    userLog = userIngresado

    # en los htmls se declara un metodo post que se dispara cuando precionan el boton de login
    if request.method == 'POST':
        try:
            noCuenta = request.form['noCuenta']
            montoPago = request.form['monto']
            descripcion = request.form['descripcion']

            # valida que los campos esten declarados
            if noCuenta and montoPago:
                # All Good, let's call MySQL
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.callproc('sp_credito', (int(cuentaIngresado), float(montoPago), int(noCuenta), descripcion))
                conn.commit()
                #  data = cursor.fetchall()

            else:
                return json.dumps({'html': '<span>Enter the required fields</span>'})

        except Exception as e:
            print("ERROR")
            return json.dumps({'error': str(e)})

        finally:
            cursor.close()
            conn.close()

    return render_template('credito.html',cuentaLog=cuentaLog, userLog=userLog)


@app.route('/debito', methods=['POST', 'GET'])
def debito():

    cuentaLog = cuentaIngresado
    userLog = userIngresado

    # en los htmls se declara un metodo post que se dispara cuando precionan el boton de login
    if request.method == 'POST':
        try:
            noCuenta = request.form['noCuenta']
            montoPago = request.form['monto']
            descripcion = request.form['descripcion']

            # valida que los campos esten declarados
            if noCuenta and montoPago:
                # All Good, let's call MySQL
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.callproc('sp_debito', (int(cuentaIngresado), float(montoPago), int(noCuenta), descripcion))
                conn.commit()
                #  data = cursor.fetchall()

            else:
                return json.dumps({'html': '<span>Enter the required fields</span>'})

        except Exception as e:
            print("ERROR")
            return json.dumps({'error': str(e)})

        finally:
            cursor.close()
            conn.close()

    return render_template('debito.html',cuentaLog=cuentaLog, userLog=userLog)





@app.route('/')
def principal():
    return render_template('principal.html')


if __name__ == '__main__':
    app.secret_key = 'some secret key'
    app.run(debug=True)
