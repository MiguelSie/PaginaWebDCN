from flask import Flask

app = Flask(__name__)

@app.route("/")
@app.route("/inicio")
def inicio():
    return "Página de bienvenida - visión, misión, valores, historia"

@app.route ("/sedes")
def sedes():
    return ("Información de sedes y ubicaciones")

@app.route ("/contacto")
def contacto():
    return ("Información de contacto")

@app.route ("/servicios")
def servicios():
    return ("Servicios que ofrece la empresa")

@app.route ("/ferias")
def ferias():
    return ("Calendario de ferias")

@app.route ("/proveedores")
def proveedores():
    return ("Ingreso de proveedores para ver su calendario")


#Aún pueden faltar rutas y definir bien las existentes. Tenemos que crear la forma de el token único de los proveedores,
#averiguar la forma de definir calendarios en la aplicación y definir una template HTML
#Módulo admin