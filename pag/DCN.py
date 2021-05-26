from flask import render_template, url_for, flash, redirect

from pag import app

#en las rutas se usa el redender para redirigir pag una pagina html
@app.route("/")
@app.route("/inicio")
def inicio():
    return render_template("PPrincipal.html")


@app.route ("/sedes")
def sedes():
    return render_template("sedes.html", title="Sedes") #Se pasa el html y el titulo de la pagina


@app.route ("/contacto")
def contacto():
    return render_template("contacto.html", title="Contacto")


@app.route ("/servicios")
def servicios():
    return render_template("servicios.html", title="Servicios")


@app.route ("/ferias")
def ferias():
    return render_template("ferias.html", title="Ferias")


@app.route ("/proveedores")
def proveedores():
    return render_template("proveedores.html", title="Proveedores")


@app.route ("/administrador")
def administrador():
    return render_template("administrador.html", title="Administrador")


#Aún pueden faltar rutas y definir bien las existentes. Tenemos que crear la forma de el token único de los proveedores,
#averiguar la forma de definir calendarios en la aplicación y definir una template HTML
#Módulo admin