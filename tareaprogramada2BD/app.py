from flask import Flask, render_template, request
import pyodbc
app = Flask(__name__)
#---------Conexion a la base de datos---------
def conectarBD():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=25.22.142.64;"
        "DATABASE=tareaProgramada1;"
        "UID=TDBD1;"
        "PWD=1234"
    )

# ----------Página principal HTML/Flask-------
@app.route("/")
def inicio():
    BD=conectarBD()
    cursor=BD.cursor()
    cursor.execute("EXEC dbo.obtenerEmpleados")
    empleados = cursor.fetchall()
    BD.close()
    return render_template("browserTareaBD.html",empleados=empleados)

# Página del formulario
@app.route("/insertar")
def insertar():
    return render_template("formulario.html")

# Procesar datos
@app.route("/procesar", methods=["POST"])
def procesar():
    nombre = request.form["nombre"]
    salario = request.form["salario"]

    return f"Empleado {nombre} agregado con salario {salario}"

if __name__ == "__main__":
    app.run(debug=True)