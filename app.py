from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = "c400768b9de13da17ee1c3855dc62d29eeb61d401a6accf101e324670fd65952"

UPLOAD_FOLDER = "static/images"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Usuarios de ejemplo (luego se pasa a BD)
usuarios = {
    "admin": {"password": "admin123", "rol": "admin"},
    "user": {"password": "user123", "rol": "usuario"}
}

# Datos de imágenes (temporal, luego BD)
imagenes = []

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["usuario"]
        pwd = request.form["password"]

        if user in usuarios and usuarios[user]["password"] == pwd:
            session["usuario"] = user
            session["rol"] = usuarios[user]["rol"]
            return redirect(url_for("galeria"))
    return render_template("login.html")

# ---------------- GALERÍA ----------------
@app.route("/galeria")
def galeria():
    if "usuario" not in session:
        return redirect(url_for("login"))

    return render_template(
        "index.html",
        imagenes=imagenes,
        rol=session["rol"]
    )

# ---------------- ADMIN ----------------
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if session.get("rol") != "admin":
        return redirect(url_for("galeria"))

    if request.method == "POST":
        file = request.files["imagen"]
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        imagenes.append({
            "nombre": request.form["nombre"],
            "modelo": request.form["modelo"],
            "serie": request.form["serie"],
            "cantidad": request.form["cantidad"],
            "sitio": request.form["sitio"],
            "archivo": filename
        })

    return render_template("admin.html", imagenes=imagenes)


# ---------------- BORRAR ----------------
@app.route("/borrar/<int:id>")
def borrar(id):
    if session.get("rol") != "admin":
        return redirect(url_for("galeria"))

    img = imagenes.pop(id)
    os.remove(os.path.join(app.config["UPLOAD_FOLDER"], img["archivo"]))
    return redirect(url_for("admin"))

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run()
