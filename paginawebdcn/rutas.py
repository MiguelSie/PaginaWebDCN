from flask import render_template, url_for, flash, redirect
from paginawebdcn.forms import RegistroProveedor, IngresoProveedor
from paginawebdcn import app, db, bcrypt
from paginawebdcn.ModelosDB import Proveedor
from flask_login import login_user, logout_user, current_user, login_required


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
    if current_user.is_authenticated:
        return redirect(url_for('inicio'))
    formulario = IngresoProveedor()
    if formulario.validate_on_submit():
        proveedor = Proveedor.query.filter_by(username=formulario.username.data).first()
        if proveedor and bcrypt.check_password_hash(proveedor.password, formulario.password.data):
            login_user(proveedor)
            flash(f"{proveedor.name} ha ingresado exitosamente ", "success")
            return redirect(url_for("inicio"))
        else:
            flash(f"El token ingresado no se encuentra registrado", "danger")
    return render_template("proveedores.html", title="Proveedores", formulario=formulario)


@app.route("/administrador", methods=['GET', 'POST'])
def administrador():
    if current_user.is_authenticated:
        return redirect(url_for('inicio'))
    formulario = RegistroProveedor()
    if formulario.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(formulario.password.data).decode('utf-8')
        proveedor = Proveedor(name=formulario.name.data, username=formulario.username.data, email=formulario.email.data,
                              password=hashed_password)
        db.session.add(proveedor)
        db.session.commit()
        flash(f' {formulario.username.data} se ha agregado exitosamente ', 'success')
        return redirect(url_for('inicio'))
    return render_template("administrador.html", title="Administrador", formulario=formulario)


@app.route("/cerrarSesion")
def cerrarSesion():
    logout_user()
    return redirect(url_for('inicio'))


@app.route("/sesionProveedor")
@login_required
def sesionProveedor():
    return render_template("sesionProv.html", title=current_user.name)


@app.route("/informacion")
def informacion():
    return render_template("informacion.html", title="Ferias")
