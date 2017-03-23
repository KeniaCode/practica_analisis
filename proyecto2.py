from flask import Flask, render_template, redirect, url_for, request, jsonify

import uuid
app = Flask(__name__)





@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    usuarioexist=False
    if request.method == 'POST':

    	codigo = request.form['cod']
        usuario = request.form['user']
        contrasenia = request.form['pass']
   
        if usuario == 'admin':
            return redirect(url_for('ingresado'))
       

    return render_template('login.html',error=error)





#*********************************************************Eleccion AREA*******************



@app.route('/depMenu')
def eleMenu():
	return render_template('depMenu.html')

@app.route('/Registrar')
def registrarse():
	return render_template('registrarse.html')

#*********************************************************************************************



#**********************************************

@app.route('/reportesMenu',methods=['GET','POST'])
def reportesMenu():
	return render_template('reportesTable.html')

#****************************************************************

@app.route('/ingresado')
def ingresado():
	return render_template('ingresado.html')

@app.route('/')
def principal():
	return render_template('principal.html')



if __name__ == '__main__':
	app.run(debug=True)
