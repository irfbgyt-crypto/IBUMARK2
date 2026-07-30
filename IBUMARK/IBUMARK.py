# ==========================================
# 💪 IBUMARK PERFORMANCE
# Parte 1
# ==========================================

import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, session

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE_DIR, "database.db")

app = Flask(__name__)
app.secret_key = "ibumarkperformance"

# ==========================================
# BASE DE DATOS
# ==========================================

def crear_db():
    print(">>> crear_db ejecutándose...") 
    import os

    print("Creando:", os.path.abspath("database.db"))
    conexion = sqlite3.connect(DB)
    cursor = conexion.cursor()
    print(">>> tablas creadas")
    # ==========================
    # MEDIDAS
    # ==========================

    cursor.execute("""
CREATE TABLE IF NOT EXISTS medidas(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario_id INTEGER,

    peso REAL,

    pecho REAL,

    cintura REAL,

    brazo REAL,

    pierna REAL,

    fecha TEXT

)
""")

    # ==========================
    # EJERCICIOS
    # ==========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ejercicios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        grupo TEXT,
        descripcion TEXT,
        imagen TEXT
    )
    """)

    # ==========================
    # RUTINAS
    # ==========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rutinas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        grupo TEXT,
        ejercicio TEXT,
        series INTEGER,
        repeticiones INTEGER
    )
    """)

    # ==========================
    # USUARIOS
    # ==========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    correo TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
 )
 """)

    conexion.commit()
    conexion.close()

# ==========================================
# RUTINAS (NO SQLITE)
# ==========================================

RUTINAS = {

    "Pecho":[

        ("Press banca",4,10),
        ("Press inclinado",4,12),
        ("Aperturas",3,15),
        ("Fondos",3,12)

    ],

    "Espalda":[

        ("Dominadas",4,10),
        ("Jalón al pecho",4,12),
        ("Remo con barra",4,10),
        ("Pullover",3,15)

    ],

    "Hombro":[

        ("Press militar",4,10),
        ("Elevaciones laterales",4,15),
        ("Pájaros",3,15)

    ],

    "Biceps":[

        ("Curl barra",4,10),
        ("Curl alterno",4,12),
        ("Martillo",3,15)

    ],

    "Triceps":[

        ("Fondos",4,12),
        ("Extensión polea",4,10),
        ("Francés",3,15)

    ],

    "Pierna":[

        ("Sentadilla",4,10),
        ("Prensa",4,12),
        ("Extensiones",3,15),
        ("Femoral",3,12)

    ],

    "Abdomen":[

        ("Crunch",4,20),
        ("Elevaciones",4,15),
        ("Plancha",3,"60 segundos")

    ]

}



# ==========================================
# BIBLIOTECA
# ==========================================

EJERCICIOS = [

{
    "nombre": "Press banca",

    "grupo": "Pecho",

    "descripcion": "Ejercicio compuesto para desarrollar fuerza y masa muscular en el pecho.",

    "imagen": "press_banca.jpg",

    "musculos": [
        "Pectoral mayor",
        "Deltoides anterior",
        "Tríceps"
    ],

    "consejos": [
        "Mantén los pies firmes en el suelo.",
        "Aprieta las escápulas antes de bajar la barra.",
        "Controla el movimiento en todo momento."
    ],

    "errores": [
        "Rebotar la barra sobre el pecho.",
        "Abrir demasiado los codos.",
        "Levantar la espalda del banco."
    ],

    "video": "https://youtu.be/TAH8RxOS0VI?si=hk-rWYS26mMhTQWu"
},

{
    "nombre": "Press inclinado",

    "grupo": "Pecho",

    "descripcion": "Ejercicio enfocado en desarrollar la parte superior del pecho.",

    "imagen": "press_inclinado.jpg",

    "musculos": [
        "Pectoral superior",
        "Deltoides anterior",
        "Tríceps"
    ],

    "consejos": [
        "Mantén el banco entre 30° y 45°.",
        "Controla la bajada.",
        "Empuja de forma explosiva."
    ],

    "errores": [
        "Inclinar demasiado el banco.",
        "Bloquear completamente los codos.",
        "Perder estabilidad."
    ],

    "video": "https://youtube.com/shorts/-zbesyTNztQ?si=bWlAUHgCTy8ArTTz"
},

{
    "nombre":"Aperturas",

    "grupo":"Pecho",

    "descripcion":"Ejercicio de aislamiento para el pectoral.",

    "imagen":"aperturas.jpg",

    "musculos":[
        "Pectoral mayor"
    ],

    "consejos":[
        "Mantén una ligera flexión en los codos.",
        "No uses demasiado peso.",
        "Controla el recorrido."
    ],

    "errores":[
        "Estirar completamente los brazos.",
        "Cerrar las mancuernas golpeándolas.",
        "Usar impulso."
    ],

    "video":"https://youtube.com/shorts/OtW0EYqBczI?si=ThMkDIp1X7uJQPUh"
},

{
    "nombre":"Dominadas",

    "grupo":"Espalda",

    "descripcion":"Ejercicio compuesto para desarrollar toda la espalda.",

    "imagen":"dominadas.jpg",

    "musculos":[
        "Dorsal ancho",
        "Bíceps",
        "Trapecio"
    ],

    "consejos":[
        "Sube hasta pasar la barbilla.",
        "Controla el descenso.",
        "Aprieta la espalda."
    ],

    "errores":[
        "Balancear el cuerpo.",
        "No extender completamente los brazos.",
        "Usar impulso."
    ],

    "video":"https://youtube.com/shorts/BT3CSQKeEww?si=MMrSm2ObwU4ttTS3"
},

{
    "nombre":"Remo con barra",

    "grupo":"Espalda",

    "descripcion":"Ejercicio para aumentar el grosor de la espalda.",

    "imagen":"remo_barra.jpg",

    "musculos":[
        "Dorsal ancho",
        "Trapecio",
        "Romboides"
    ],

    "consejos":[
        "Mantén la espalda recta.",
        "Lleva la barra al abdomen.",
        "Aprieta la espalda arriba."
    ],

    "errores":[
        "Redondear la espalda.",
        "Usar demasiado impulso.",
        "Subir los hombros."
    ],

    "video":"https://www.youtube.com/shorts/pmJKV0pfI3M"
},

{
    "nombre":"Press militar",

    "grupo":"Hombro",

    "descripcion":"Ejercicio principal para desarrollar fuerza y volumen en los hombros.",

    "imagen":"press_militar.jpg",

    "musculos":[
        "Deltoides",
        "Tríceps",
        "Trapecio superior"
    ],

    "consejos":[
        "Mantén el abdomen contraído.",
        "Empuja la barra completamente arriba.",
        "Controla el descenso."
    ],

    "errores":[
        "Arquear demasiado la espalda.",
        "Bajar la barra muy rápido.",
        "Usar impulso con las piernas."
    ],

    "video":"https://www.youtube.com/shorts/DdITN8U-kFI"
},

{
    "nombre":"Curl barra",

    "grupo":"Biceps",

    "descripcion":"Ejercicio básico para desarrollar fuerza y tamaño del bíceps.",

    "imagen":"curl_z.jpg",

    "musculos":[
        "Bíceps braquial",
        "Braquial",
        "Braquiorradial"
    ],

    "consejos":[
        "Mantén los codos pegados al cuerpo.",
        "Sube sin balancearte.",
        "Aprieta el bíceps arriba."
    ],

    "errores":[
        "Mover la espalda.",
        "Balancear el cuerpo.",
        "No controlar la bajada."
    ],

    "video":"https://www.youtube.com/shorts/S_6T_cf65FA"
},

{
    "nombre":"Fondos",

    "grupo":"Triceps",

    "descripcion":"Ejercicio compuesto excelente para desarrollar tríceps y pecho.",

    "imagen":"fondos.jpg",

    "musculos":[
        "Tríceps",
        "Pectoral",
        "Deltoides anterior"
    ],

    "consejos":[
        "Mantén el cuerpo estable.",
        "Baja hasta formar 90°.",
        "Empuja completamente."
    ],

    "errores":[
        "Bajar demasiado.",
        "Abrir mucho los codos.",
        "Hacer rebotes."
    ],

    "video":"https://www.youtube.com/shorts/QXumck_EpRI"
},

{
    "nombre":"Sentadilla",

    "grupo":"Pierna",

    "descripcion":"El ejercicio más completo para desarrollar las piernas y la fuerza general.",

    "imagen":"sentadilla.jpg",

    "musculos":[
        "Cuádriceps",
        "Glúteos",
        "Femoral"
    ],

    "consejos":[
        "Mantén la espalda recta.",
        "Empuja con los talones.",
        "Baja hasta romper el paralelo."
    ],

    "errores":[
        "Levantar los talones.",
        "Redondear la espalda.",
        "Juntar las rodillas."
    ],

    "video":"https://www.youtube.com/shorts/70R4P-Oj0MM"
},

{
    "nombre":"Crunch",

    "grupo":"Abdomen",

    "descripcion":"Ejercicio de aislamiento para fortalecer la parte superior del abdomen.",

    "imagen":"crunch.jpg",

    "musculos":[
        "Recto abdominal"
    ],

    "consejos":[
        "Contrae el abdomen al subir.",
        "No jales el cuello.",
        "Realiza el movimiento lentamente."
    ],

    "errores":[
        "Impulsarse con el cuello.",
        "Subir demasiado el torso.",
        "Hacer el movimiento muy rápido."
    ],

    "video":"https://www.youtube.com/shorts/XuQWMR4QKF0?feature=share"
}

]

# ==========================================
# HOME
# ==========================================



@app.route("/")
def home():

    if "usuario_id" not in session:
        return redirect("/login")

    import os

    print("Base de datos:", os.path.abspath("database.db"))

    conexion = sqlite3.connect(DB)
    cursor = conexion.cursor()

    # Último registro
    usuario = session["usuario_id"]

    cursor.execute("""
    SELECT peso, fecha
    FROM medidas
    WHERE usuario_id=?
    ORDER BY id DESC
    LIMIT 1
    """,(usuario,))

    ultimo = cursor.fetchone()

    if ultimo:
        peso = ultimo[0]
        fecha = ultimo[1]
    else:
        peso = "--"
        fecha = "--"

    # Total de rutinas
    cursor.execute("""
    SELECT COUNT(DISTINCT grupo)
    FROM rutinas
    """)

    total_rutinas = cursor.fetchone()[0]

    # Total de ejercicios
    cursor.execute("""
    SELECT COUNT(*)
    FROM ejercicios
    """)

    total_ejercicios = cursor.fetchone()[0]

    conexion.close()

    from datetime import datetime

    hoy = datetime.now()

    fecha_actual = hoy.strftime("%d/%m/%Y")

    if hoy.hour < 12:
     saludo = "☀️ Buenos días"

    elif hoy.hour < 19:
     saludo = "🌤️ Buenas tardes"

    else:
     saludo = "🌙 Buenas noches"

    return render_template(
    "index.html",
    peso=peso,
    fecha=fecha,
    total_rutinas=total_rutinas,
    total_ejercicios=total_ejercicios,
    saludo=saludo,
    fecha_actual=fecha_actual,
    usuario=session.get("usuario_nombre")
)

# ==========================================
# MEDIDAS
# ==========================================

@app.route("/medidas")
def medidas():
    
    


    conexion = sqlite3.connect(DB)
    cursor = conexion.cursor()

    usuario = session["usuario_id"]

    cursor.execute("""

    SELECT *

    FROM medidas

    WHERE usuario_id=?

    ORDER BY id DESC

    """,(usuario,))

    datos = cursor.fetchall()

    conexion.close()

    return render_template(
        "medidas.html",
        datos=datos
    )


@app.route("/eliminar_medida/<int:id>")
def eliminar_medida(id):

    conexion = sqlite3.connect(DB)
    cursor = conexion.cursor()

    cursor.execute(
        "DELETE FROM medidas WHERE id=?",
        (id,)
    )

    conexion.commit()
    conexion.close()

    flash("Registro eliminado correctamente.", "success")

    return redirect("/medidas")


@app.route("/editar_medida/<int:id>")
def editar_medida(id):

    conexion = sqlite3.connect(DB)
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT * FROM medidas WHERE id=?",
        (id,)
    )

    dato = cursor.fetchone()

    conexion.close()

    return render_template(
        "editar_medida.html",
        dato=dato
    )


@app.route("/actualizar_medida/<int:id>", methods=["POST"])
def actualizar_medida(id):

    peso = request.form["peso"]
    pecho = request.form["pecho"]
    cintura = request.form["cintura"]
    brazo = request.form["brazo"]
    pierna = request.form["pierna"]

    conexion = sqlite3.connect(DB)
    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE medidas
        SET
            peso=?,
            pecho=?,
            cintura=?,
            brazo=?,
            pierna=?
        WHERE id=?
    """,
    (
        peso,
        pecho,
        cintura,
        brazo,
        pierna,
        id
    ))

    conexion.commit()
    conexion.close()

    flash("Registro actualizado correctamente.","success")

    return redirect("/medidas")

# ==========================================
# AGREGAR MEDIDAS
# ==========================================

@app.route("/agregar_medidas", methods=["POST"])
def agregar_medidas():

    conexion = sqlite3.connect(DB)
    cursor = conexion.cursor()

    fecha = datetime.now().strftime("%d/%m/%Y")

    usuario = session["usuario_id"]

    cursor.execute("""

    INSERT INTO medidas

    (usuario_id,peso,pecho,cintura,brazo,pierna,fecha)

    VALUES(?,?,?,?,?,?,?)

    """,(

        usuario,
        request.form["peso"],
        request.form["pecho"],
        request.form["cintura"],
        request.form["brazo"],
        request.form["pierna"],
        fecha

    ))

    conexion.commit()
    conexion.close()

    flash("✅ Medidas registradas correctamente","success")

    return redirect("/medidas")

# ==========================================
# 💪 RUTINAS
# ==========================================

@app.route("/rutina")
def rutina():

    if "usuario_id" not in session:
     return redirect("/login")

    grupos = list(RUTINAS.keys())

    return render_template(
        "rutina.html",
        grupos=grupos
    )

# ==========================================
# 💪 ejercicio
# ==========================================

@app.route("/ejercicio/<int:id>")
def ejercicio(id):

    ejercicio = EJERCICIOS[id]

    return render_template(
        "ejercicio.html",
        ejercicio=ejercicio
    )

# ==========================================
# 📋 DETALLE DE RUTINA
# ==========================================

@app.route("/rutina/<grupo>")
def detalle_rutina(grupo):

    ejercicios = RUTINAS.get(grupo, [])

    return render_template(
        "detalle_rutina.html",
        grupo=grupo,
        ejercicios=ejercicios
    )


# ==========================================
# 📚 BIBLIOTECA DE EJERCICIOS
# ==========================================

@app.route("/ejercicios")
def ejercicios():

    return render_template(
        "ejercicios.html",
        ejercicios=EJERCICIOS
    )


# ==========================================
# 📈 PROGRESO
# ==========================================

@app.route("/progreso")
def progreso():

    if "usuario_id" not in session:
     return redirect("/login")

    conexion = sqlite3.connect(DB)
    cursor = conexion.cursor()

    usuario = session["usuario_id"]

    cursor.execute("""
    SELECT fecha,peso,pecho,cintura,brazo,pierna
    FROM medidas
    WHERE usuario_id=?
    ORDER BY id
    """,(usuario,))

    datos = cursor.fetchall()

    conexion.close()

    fechas = [d[0] for d in datos]
    pesos = [d[1] for d in datos]
    pechos = [d[2] for d in datos]
    cinturas = [d[3] for d in datos]
    brazos = [d[4] for d in datos]
    piernas = [d[5] for d in datos]

    return render_template(
        "progreso.html",
        fechas=fechas,
        pesos=pesos,
        pechos=pechos,
        cinturas=cinturas,
        brazos=brazos,
        piernas=piernas
    )

# ==========================================
# ❓ AYUDA
# ==========================================

@app.route("/ayuda")
def ayuda():

    if "usuario_id" not in session:
     return redirect("/login")

    consejos = [

        "Entrena con una técnica correcta.",

        "Descansa entre 7 y 9 horas.",

        "Mantente hidratado.",

        "Consume suficiente proteína.",

        "Lleva un registro de tus avances."

    ]

    return render_template(
        "ayuda.html",
        consejos=consejos
    )

# ==========================================
# REGISTRO
# ==========================================

print("RUTA REGISTRO CARGADA")

@app.route("/registro")
def registro():
    return render_template("registro.html")

# ==========================================
# LOGIN
# ==========================================

@app.route("/login")
def login():

    return render_template("login.html")

@app.route("/iniciar_sesion", methods=["POST"])
def iniciar_sesion():

    correo = request.form["correo"]
    password = request.form["password"]

    conexion = sqlite3.connect(DB)
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT id,nombre
    FROM usuarios
    WHERE correo=? AND password=?
    """,(correo,password))

    usuario = cursor.fetchone()

    conexion.close()

    if usuario:

        session["usuario_id"] = usuario[0]
        session["usuario_nombre"] = usuario[1]

        flash("Bienvenido " + usuario[1], "success")

        return redirect("/")

    flash("Correo o contraseña incorrectos.","danger")

    return redirect("/login")

# ==========================================
# CERRAR SESIÓN
# ==========================================

@app.route("/logout")
def logout():

    session.clear()

    flash("Sesión cerrada correctamente.", "success")

    return redirect("/login")


@app.route("/registrar_usuario", methods=["POST"])
def registrar_usuario():

    nombre = request.form["nombre"]
    correo = request.form["correo"]
    password = request.form["password"]

    conexion = sqlite3.connect(DB)
    cursor = conexion.cursor()

    try:

        cursor.execute("""
        INSERT INTO usuarios
        (nombre, correo, password)
        VALUES (?, ?, ?)
        """, (
            nombre,
            correo,
            password
        ))

        conexion.commit()

        flash("Cuenta creada correctamente.", "success")

    except sqlite3.IntegrityError:

        flash("Ese correo ya está registrado.", "danger")

    finally:

        conexion.close()

    return redirect("/login")

    conexion.commit()
    conexion.close()

    flash("Cuenta creada correctamente.", "success")

    return redirect("/login")

# ==========================================
# 🚀 INICIALIZAR BASE DE DATOS
# ==========================================

crear_db()

# ==========================================
# 🚀 EJECUTAR APLICACIÓN
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )