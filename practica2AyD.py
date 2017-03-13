from flask import Flask, render_template, redirect, url_for, request, json
from flask_restful import Api
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'mydb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
api = Api(app)

# aqui vamos a guardar el usuario y su codigo
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
        print("entro al if")

        codigoI = request.form['cod']
        usuario = request.form['user']
        contrasenia = request.form['pass']
        # valida que los campos esten declarados
        if usuario and contrasenia:
            print("entro al if")
            # All Good, let's call MySQL
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_login', (codigoI, usuario, contrasenia))
            data = cursor.fetchall()
            for row in data:
                print str(row[2])

            # el procedimiento de sql retorno que no se contro al usuario
            if len(data) is 0:
                conn.commit()
                print("usuario incorrecto")
                return json.dumps({'message': 'Usuario incorrecto !'})
            else:
                print("usuario correcto" + str(data[0]))

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
                print("entro al if")
                # All Good, let's call MySQL
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.callproc('sp_registro', (usuarioN, passU, nombreU, emailU))
                data = cursor.fetchall()

                # el procedimiento de sql retorno que no se contro al usuario
                if len(data) is 0:
                    conn.commit()
                    print("registro EXITOSO")
                else:
                    print("registro FALLIDO")

            else:
                return json.dumps({'html': '<span>Enter the required fields</span>'})


        except Exception as e:
            return json.dumps({'error': str(e)})
        finally:
            cursor.close()
            conn.close()

    return render_template('registrarse.html')


# *********************************************************************************************
@app.route('/testing')
def testing():
    return 'user: ' + userIngresado


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

    # en los htmls se declara un metodo post que se dispara cuando precionan el boton de login
    if request.method == 'POST':
        try:
            tipo = request.form['idCombo']
            noCuenta = request.form['noCuenta']
            montoPago = request.form['montoPago']
            # valida que los campos esten declarados
            if noCuenta and montoPago:
                print("entro al if")
                # All Good, let's call MySQL
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.callproc('sp_pago_servicios', (cuentaIngresado, montoPago, noCuenta, tipo))
                data = cursor.fetchall()

            else:
                return json.dumps({'html': '<span>Enter the required fields</span>'})


        except Exception as e:
            return json.dumps({'error': str(e)})
            print("ERROR")

        finally:
            cursor.close()
            conn.close()

    return render_template('pagoServicios.html', l=l)


@app.route('/')
def principal():
    return render_template('principal.html')


if __name__ == '__main__':
    app.run(debug=True)
