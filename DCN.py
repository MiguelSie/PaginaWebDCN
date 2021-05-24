from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistroProveedor, IngresoProveedor

# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '7a80b6dd33a8ada86f05d3e4bce3ecf9'


# en las rutas se usa el redender para redirigir a una pagina html
@app.route("/")
@app.route("/inicio")
def inicio():
    return render_template("PPrincipal.html")


@app.route("/sedes")
def sedes():
    return render_template("sedes.html", title="Sedes")  # Se pasa el html y el titulo de la pagina


@app.route("/contacto")
def contacto():
    return render_template("contacto.html", title="Contacto")


@app.route("/servicios")
def servicios():
    return render_template("servicios.html", title="Servicios")


@app.route("/ferias")
def ferias():
    return render_template("ferias.html", title="Ferias")


@app.route("/proveedores", methods=['GET', 'POST'])
def proveedores():
    formulario = IngresoProveedor()
    if formulario.validate_on_submit():
        if formulario.password.data == "123":
            flash(f" EL LOCO ha ingresado exitosamente ", "success")
            return redirect(url_for("inicio"))
        else:
            flash(f"El token ingresado no se encuentra registrado", "danger")
    return render_template("proveedores.html", title="Proveedores", formulario=formulario)


@app.route("/administrador", methods=['GET', 'POST'])
def administrador():
    formulario = RegistroProveedor()
    if formulario.validate_on_submit():
        flash(f' {formulario.username.data} se ha agregado exitosamente ', 'success')
        return redirect(url_for('administrador'))
    return render_template("administrador.html", title="Administrador", formulario=formulario)


if __name__ == '__main__':
    app.run(debug=True)

# Aún pueden faltar rutas y definir bien las existentes. Tenemos que crear la forma de el token único de los proveedores,
# averiguar la forma de definir calendarios en la aplicación y definir una template HTML
# Módulo admin
