from flask import Flask, render_template, request, redirect, url_for, flash, session

from config import PAGE_TITLE, SECRET_KEY, AUTH_USER
from controllers.cliente_controller import ClienteController
from controllers.auth_controller import AuthController

app = Flask(__name__)
app.secret_key = SECRET_KEY
controller = ClienteController()


def login_required(view):
    def wrapped_view(**kwargs):
        if not session.get("authenticated"):
            return redirect(url_for("login"))
        return view(**kwargs)
    wrapped_view.__name__ = view.__name__
    return wrapped_view


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        auth = AuthController()
        if auth.login(username, password):
            session["authenticated"] = True
            flash("Sesión iniciada correctamente.", "success")
            return redirect(url_for("dashboard"))
        flash("Usuario o contraseña incorrectos.", "danger")

    return render_template("login.html", title=PAGE_TITLE)


@app.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada.", "info")
    return redirect(url_for("login"))


@app.route("/")
@app.route("/dashboard")
@login_required
def dashboard():
    clientes = controller.listar()
    total = len(clientes)
    activos = int((clientes["Activo"] == True).sum()) if total else 0
    inactivos = total - activos
    return render_template(
        "dashboard.html",
        title=PAGE_TITLE,
        total=total,
        activos=activos,
        inactivos=inactivos,
        connected=controller.is_connected(),
    )


@app.route("/clientes", methods=["GET", "POST"])
@login_required
def clientes():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        correo = request.form.get("correo", "").strip()
        telefono = request.form.get("telefono", "").strip()
        if nombre and correo and telefono:
            controller.guardar(nombre, correo, telefono)
            flash("Cliente agregado correctamente.", "success")
            return redirect(url_for("clientes"))
        flash("Complete todos los campos antes de guardar.", "warning")

    clientes_df = controller.listar()
    clientes_list = clientes_df.to_dict(orient="records")
    return render_template(
        "clientes.html",
        title="Clientes",
        clientes=clientes_list,
        connected=controller.is_connected(),
    )


@app.route("/clientes/editar/<int:cliente_id>", methods=["GET", "POST"])
@login_required
def editar_cliente(cliente_id):
    cliente = controller.obtener(cliente_id)
    if cliente is None:
        flash("Cliente no encontrado.", "danger")
        return redirect(url_for("clientes"))

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        correo = request.form.get("correo", "").strip()
        telefono = request.form.get("telefono", "").strip()
        if nombre and correo and telefono:
            controller.actualizar(cliente_id, nombre, correo, telefono)
            flash("Cliente actualizado correctamente.", "success")
            return redirect(url_for("clientes"))
        flash("Complete todos los campos antes de actualizar.", "warning")

    return render_template("clientes.html", title="Editar cliente", cliente=cliente, clientes=controller.listar().to_dict(orient="records"))


@app.route("/clientes/eliminar/<int:cliente_id>")
@login_required
def eliminar_cliente(cliente_id):
    controller.eliminar(cliente_id)
    flash("Cliente eliminado.", "info")
    return redirect(url_for("clientes"))


@app.route("/clientes/inactivar/<int:cliente_id>")
@login_required
def inactivar_cliente(cliente_id):
    controller.toggle_activo(cliente_id)
    flash("Estado del cliente actualizado.", "success")
    return redirect(url_for("clientes"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8501, debug=True)
