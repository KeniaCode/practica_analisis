from flask import Flask, render_template, request, json
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'mydb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/showLogin')
def showLogin():
    return render_template('login.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    try:
        usuario = request.form['user']
        contrasenia = request.form['pass']
        # validate the received values
        if usuario and contrasenia:
            print("entro al if")
            # All Good, let's call MySQL
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_login', (usuario, contrasenia))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                print("usuario incorrecto")
                return json.dumps({'message': 'User created successfully !'})
            else:
                print("usuario correcto")
                return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor.close()
        conn.close()

#*********************************************************Eleccion AREA*******************



@app.route('/depMenu')
def eleMenu():
	return render_template('depMenu.html')


#*********************************************************************************************



@app.route('/reportesMenu',methods=['GET','POST'])
def reportesMenu():
	return render_template('reportesTable.html')

#****************************************************************

@app.route('/')
def principal():
	return render_template('principal.html')


if __name__ == '__main__':app.run(debug=True)



