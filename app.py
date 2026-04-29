from flask import Flask, redirect, render_template, request
import pyodbc
app = Flask(__name__)
#---------Conexion a la base de datos---------
def conectarBD():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=25.22.142.64;"
        "DATABASE=tareaProgramada2;"
        "UID=TDBD1;"
        "PWD=1234"
    )
#-------------Pagina de login----------------
@app.route("/", methods=["GET","POST"])
def Login():
    return render_template("loginTarea.html")

@app.route("/login", methods=["POST"])
def procesarLogin():
    usuario = request.form["Username"]
    contraseña = request.form["Password"]
    BD=conectarBD()
    cursor=BD.cursor()
    cursor.execute("EXEC dbo.consultarUsuario @Username=?, @Password=?", (usuario, contraseña))
    resultado = cursor.fetchone()
    if resultado is None:
        BD.close()
        return "Error: no se recibió resultado"
    result = resultado[0]
    if result==50001:
        BD.close()
        mensaje = "Error: Usuario no existe."
        return render_template("loginTarea.html", mensaje=mensaje)
    if result==50002:
        BD.close()
        mensaje = "Error: Contraseña incorrecta."
        return render_template("loginTarea.html", mensaje=mensaje)
    BD.commit()
    BD.close()
    return redirect("/principal")
# ----------Página principal HTML/Flask-------
@app.route("/principal")
def inicio():
    BD=conectarBD()
    cursor=BD.cursor()
    cursor.execute("EXEC dbo.consultarEmpleados")
    empleados = cursor.fetchall()
    cursor.execute("EXEC dbo.consultarPuestos")
    puestos = cursor.fetchall()
    BD.close()
    return render_template("browserTareaBD.html",empleados=empleados,puestos=puestos)
@app.route("/filtrar", methods=["GET","POST"])
def filtrar():
    filtro = request.form["filtro"]
    BD=conectarBD()
    cursor=BD.cursor()
    if not filtro or filtro.strip() == "":
        return redirect("/principal")
    cursor.execute("EXEC dbo.filtrarEmpleados @Filtro=?", (filtro,))
    empleados = cursor.fetchall()
    cursor.execute("EXEC dbo.consultarPuestos")
    puestos = cursor.fetchall()
    BD.close()
    return render_template("browserTareaBD.html",empleados=empleados,puestos=puestos)
# Página del formulario
@app.route("/insertar")
def insertar():
    BD=conectarBD()
    cursor=BD.cursor()
    cursor.execute("EXEC dbo.consultarPuestos")
    puestos = cursor.fetchall()
    BD.close()
    return render_template("formulario.html",puestos=puestos)

@app.route("/eliminar", methods=["POST"])
def eliminar():
    id = request.form["empleado"]
    BD=conectarBD()
    cursor=BD.cursor()
    cursor.execute("EXEC dbo.borrarEmpleado @Id=?", (id,))
    BD.commit()
    BD.close()
    return redirect("/principal")
@app.route("/actualizar", methods=["POST"])
def actualizar():
    id = request.form["empleado"]
    nombre=request.form["nombre"]
    docIden=request.form["documento"]
    puesto=request.form["puesto"]
    BD=conectarBD()
    cursor=BD.cursor()
    cursor.execute("""EXEC dbo.ActualizarEmpleado @Id=?, @IdPuesto=?,@ValorDocIden=?,@Nombre=?""", (id,puesto,docIden,nombre))
    BD.commit()
    BD.close()
    return redirect("/principal")
# Procesar datos
@app.route("/procesar", methods=["POST"])
def procesar():
    nombre = request.form["nombre"]
    docIden = request.form["docIden"]
    puesto = request.form["puesto"]
    if not nombre.replace(" ", "").isalpha():
        mensaje = "Error: El nombre debe contener solo letras."
        return render_template("formulario.html", mensaje=mensaje)
    if not docIden.isdigit():
        mensaje = "Error: El documento de identidad debe ser un número."
        return render_template("formulario.html", mensaje=mensaje)
    else:
        BD=conectarBD()
        cursor=BD.cursor()
        cursor.execute("""DECLARE @ret INT;EXEC @ret = dbo.InsertarEmpleado @IdPuesto=?,@ValorDocumentoIdentidad=?,@Nombre=?;SELECT @ret;""", (puesto,docIden,nombre))
        resultado = cursor.fetchone()
        if resultado is None:
            BD.close()
            return "Error: no se recibió resultado"
        result = resultado[0]
        if result==-1:
            BD.close()
            mensaje = "Error: El empleado ya existe."
            return render_template("formulario.html", mensaje=mensaje)
        BD.commit()
        BD.close()
        return redirect("/principal")
@app.route("/movimientos",methods =["GET","POST"])
def movimientos():
    if request.method == "POST":
        id = request.form["empleado"]
    else:
        id = request.args.get("id")
    BD = conectarBD()
    cursor = BD.cursor()

    cursor.execute("EXEC listarMovimientos ?", (id,))

    empleado = cursor.fetchone()

    cursor.nextset()
    movimientos = cursor.fetchall()

    BD.close()

    return render_template(
        "movimientos.html",
        empleado=empleado,
        movimientos=movimientos,
        idEmpleado=id
    )

@app.route("/insertarMovimiento/<int:id>")
def insertar_movimiento(id):
    BD = conectarBD()
    cursor = BD.cursor()

    # Obtener tipos de movimiento (para dropdown)
    cursor.execute("SELECT Id, Nombre FROM TipoMovimiento")
    tipos = cursor.fetchall()

    BD.close()

    return render_template("insertarMovimiento.html",
                           idEmpleado=id,
                           tipos=tipos)

@app.route("/guardarMovimiento", methods=["POST"])
def guardar_movimiento():
    IdEmpleado = request.form["IdEmpleado"]
    IdTipoMovimiento = request.form["IdTipoMovimiento"]
    Monto = request.form["Monto"]

    # ⚠️ por ahora valores fijos (luego login)
    IdUsuario = 1
    IP = 123456  # si usas INT

    BD = conectarBD()
    cursor = BD.cursor()

    cursor.execute(
        "EXEC insertarMovimiento ?, ?, ?, ?, ?",
        (IdEmpleado, IdTipoMovimiento, Monto, IdUsuario, IP)
    )

    BD.commit()
    BD.close()

    # volver a ver movimientos del mismo empleado
    return redirect(f"/movimientos?id={IdEmpleado}")

if __name__ == "__main__":
    app.run(debug=True)