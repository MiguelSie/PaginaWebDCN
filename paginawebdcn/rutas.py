from flask import render_template, url_for, flash, redirect, request, abort
from paginawebdcn.forms import RegistroProveedor, IngresoProveedor, IngresoAdministrador, BusquedaProv, \
    ActualizarProveedor
from paginawebdcn import app, db, bcrypt
from paginawebdcn.ModelosDB import Proveedor, Administrador
from flask_login import login_user, logout_user, current_user, login_required

admin = Administrador.query.filter_by(id=1).first()


# en las rutas se usa el redender para redirigir a una pagina html
@app.route("/")
@app.route("/inicio")
def inicio():
    return render_template("PPrincipal.html", admin=admin)


@app.route("/sedes")
def sedes():
    return render_template("sedes.html", title="Sedes", admin=admin)  # Se pasa el html y el titulo de la pagina


@app.route("/contacto")
def contacto():
    return render_template("contacto.html", title="Contacto", admin=admin)


@app.route("/servicios")
def servicios():
    return render_template("servicios.html", title="Servicios", admin=admin)


@app.route("/ferias")
def ferias():
    return render_template("ferias.html", title="Ferias", admin=admin)


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
    return render_template("proveedores.html", title="Proveedores", formulario=formulario, admin=admin)


@app.route("/administrador", methods=['GET', 'POST'])
@login_required
def administrador():
    if current_user.email == admin.email:
        formulario = RegistroProveedor()
        proveedores = Proveedor.query.all()
        if formulario.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(formulario.password.data).decode('utf-8')
            proveedor = Proveedor(name=formulario.name.data, username=formulario.username.data,
                                  email=formulario.email.data,
                                  password=hashed_password)
            db.session.add(proveedor)
            db.session.commit()
            flash(f' {formulario.username.data} se ha agregado exitosamente ', 'success')
            return redirect(url_for('administrador'))
        return render_template("administrador.html", title="Administrador", formulario=formulario,
                               proveedores=proveedores, admin=admin)
    else:
        flash(f' {current_user.username} No tiene acceso a este modulo', 'danger')
        return redirect(url_for('inicio'))


@app.route("/cerrarSesion")
def cerrarSesion():
    logout_user()
    return redirect(url_for('inicio'))


@app.route("/sesionProveedor")
@login_required
def sesionProveedor():
    return render_template("sesionProv.html", title="Calendario de compras", admin=admin)


@app.route("/informacion")
def informacion():
    return render_template("informacion.html", title="Información", admin=admin)


@app.route("/loginAdministrador", methods=['GET', 'POST'])
def loginAdministrador():
    if current_user.is_authenticated:
        return redirect(url_for('administrador'))
    formulario = IngresoAdministrador()
    if formulario.validate_on_submit():
        administrador = Administrador.query.filter_by(email=formulario.email.data).first()
        if administrador and formulario.password.data == administrador.password:
            login_user(administrador)
            flash(f"Ha ingresado exitosamente ", "success")
            return redirect(url_for("administrador"))
        else:
            flash(f"El token ingresado no se encuentra registrado", "danger")
    return render_template("loginAdmi.html", title="Iniciar sesion como administrador", formulario=formulario,
                           admin=admin)


@app.route("/LProveedores", methods=['GET', 'POST'])
@login_required
def LProveedores():
    if current_user.email == admin.email:
        formularioBusqueda = BusquedaProv()
        proveedores = Proveedor.query.all()
        if formularioBusqueda.validate_on_submit():
            proveedorB = Proveedor.query.filter_by(email=formularioBusqueda.email.data).first()
            if proveedorB:
                return redirect(url_for('proveedor', prov_id=proveedorB.id))
            else:
                flash(f' {formularioBusqueda.email.data} No fue encontrado ', 'danger')
        else:
            proveedorB = None
        return render_template("ListaProveedores.html", title="Lista de proveedores", proveedores=proveedores,
                               admin=admin,
                               formularioBusqueda=formularioBusqueda, proveedorB=proveedorB)
    else:
        flash(f' {current_user.username} No tiene acceso a este modulo', 'danger')
        return redirect(url_for('inicio'))


@app.route("/proveedor/<int:prov_id>", methods=['GET', 'POST'])
@login_required
def proveedor(prov_id):
    if current_user.email == admin.email:
        proveedorB = Proveedor.query.filter_by(id=prov_id).first()
        formularioActu = ActualizarProveedor()
        if formularioActu.validate_on_submit():
            proveedorB.name = formularioActu.name.data
            proveedorB.username = formularioActu.username.data
            proveedorB.email = formularioActu.email.data
            db.session.commit()
            flash('Se han actualizado los datos exitosamente', 'success')
            return redirect(url_for('LProveedores'))
        elif request.method == 'GET':
            formularioActu.name.data = proveedorB.name
            formularioActu.username.data = proveedorB.username
            formularioActu.email.data = proveedorB.email
        return render_template("proveedor.html", title="busqueda de proveedor", admin=admin,
                               formularioActu=formularioActu, proveedorB=proveedorB)
    else:
        flash(f' {current_user.username} No tiene acceso a este modulo', 'danger')
        return redirect(url_for('inicio'))


@app.route("/proveedor/<int:prov_id>/borrar",  methods=['GET', 'POST'])
@login_required
def eliminarProv(prov_id):
    if current_user.email == admin.email:
        proveedor = Proveedor.query.get(prov_id)
        db.session.delete(proveedor)
        db.session.commit()
        flash(f'Se ha eliminado a {proveedor.name} exitosamente de la lista', 'success')
        return redirect(url_for('LProveedores'))
    else:
        flash(f' {current_user.username} No tiene acceso a este modulo', 'danger')
        return redirect(url_for('inicio'))
