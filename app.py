from flask import Flask, render_template, request, redirect, url_for, session, send_file
from werkzeug.utils import secure_filename
import os
import openpyxl
from openpyxl.drawing.image import Image as XLImage
import io


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


@app.route("/descargar_excel")
def descargar_excel():
    # Lista de equipos (igual que la que usas en tu index)
    equipos = [
                  {'archivo': 'prod001.jpeg', 'nombre': 'Rack de Plastico', 'modelo': 'COMMSCOPE', 'serie': '760072942',
                   'cantidad': 1, 'sitio': 'BBVA'},
                  {'archivo': 'prod002.jpeg', 'nombre': 'Puertos RJ45', 'modelo': 'COMMSCOPE', 'serie': '760201145',
                   'cantidad': 1, 'sitio': 'BBVA'},
                  {'archivo': 'prod003.jpeg', 'nombre': 'Lector de Huellas Dactilares', 'modelo': 'DactyScan84c',
                   'serie': 'C8RUHU06341', 'cantidad': 5, 'sitio': 'BBVA'},
                  {'archivo': 'prod004.jpeg', 'nombre': 'Escaner de Cheques', 'modelo': 'Vision X AGP',
                   'serie': 'TA71-3001400', 'cantidad': 10, 'sitio': 'BBVA'},
                  {'archivo': 'prod005.jpeg', 'nombre': 'DVR PROVISSION ISR', 'modelo': 'SH-8200A-2L',
                   'serie': '110071EOT17281895', 'cantidad': 1, 'sitio': 'BBVA'},
                  {'archivo': 'prod006.jpeg', 'nombre': 'Teclado HP', 'modelo': 'KBAR211', 'serie': '803181-161',
                   'cantidad': 1, 'sitio': 'BBVA'},
                  {'archivo': 'prod007.jpeg', 'nombre': 'Mini PC Dell', 'modelo': 'N/A', 'serie': 'N/A', 'cantidad': 1,
                   'sitio': 'BBVA'},
                  {'archivo': 'prod008.jpeg', 'nombre': 'Varias Cosas', 'modelo': 'Varios', 'serie': 'Varios',
                   'cantidad': 5, 'sitio': 'BBVA'},
                  {'archivo': 'prod009.jpeg', 'nombre': 'Varias Cosas', 'modelo': 'Varios', 'serie': 'Varios',
                   'cantidad': 10, 'sitio': 'BBVA'},
                  {'archivo': 'prod10.jpeg', 'nombre': 'Varias Cosas', 'modelo': 'Varios', 'serie': 'Varios',
                   'cantidad': 10, 'sitio': 'BBVA'},
                  {'archivo': 'prod11.jpeg', 'nombre': 'Varias Cosas', 'modelo': 'Varios', 'serie': 'Varios',
                   'cantidad': 5, 'sitio': 'BBVA'},
                  {'archivo': 'prod12.jpeg', 'nombre': 'Varias Cosas', 'modelo': 'Varios', 'serie': 'Varios',
                   'cantidad': 10, 'sitio': 'BBVA'},
                  {'archivo': 'prod13.jpeg', 'nombre': 'Ordenador de Cables Site', 'modelo': 'PANDUIT', 'serie': 'N/A',
                   'cantidad': 1, 'sitio': 'BBVA'},
                  {'archivo': 'prod14.jpeg', 'nombre': 'Monitor HP', 'modelo': 'P223', 'serie': 'CNK80304YMT',
                   'cantidad': 1, 'sitio': 'BBVA'},
                  {'archivo': 'prod15.jpeg', 'nombre': 'Tripie Multiusos', 'modelo': 'N/A', 'serie': 'N/A',
                   'cantidad': 1, 'sitio': 'BBVA'},
                  {'archivo': 'prod16.jpeg', 'nombre': 'Monitor HP', 'modelo': 'P224', 'serie': 'CNK92807YBT',
                   'cantidad': 1, 'sitio': 'BBVA'},
                  {'archivo': 'prod17.jpeg', 'nombre': 'Impresora HP', 'modelo': 'LaserJet 4250n',
                   'serie': '4250/4350 series', 'cantidad': 1, 'sitio': 'BBVA'},
                  {'archivo': 'prod18.jpeg', 'nombre': 'Impresora Samsung', 'modelo': 'MultiXpress', 'serie': '6322DN',
                   'cantidad': 1, 'sitio': 'BBVA'},
                  {'archivo': 'prod19.jpeg', 'nombre': 'Telefono AVAYA', 'modelo': '9620', 'serie': '09FA42586867',
                   'cantidad': 1, 'sitio': 'BBVA'},
                  {'archivo': 'prod20.jpeg', 'nombre': 'Varias Cosas', 'modelo': 'Varios', 'serie': 'Varios',
                   'cantidad': 5, 'sitio': 'BBVA'},
                  {'archivo': 'prod21.jpeg', 'nombre': 'Varias Cosas', 'modelo': 'Varios', 'serie': 'Varios',
                   'cantidad': 5, 'sitio': 'BBVA'},
                  {'archivo': 'prod22.jpeg', 'nombre': 'Varias Cosas', 'modelo': 'Varios', 'serie': 'Varios',
                   'cantidad': 5, 'sitio': 'BBVA'},
    ]

    # Crear workbook y hoja
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Inventario de Equipos"

    # Definir encabezados
    headers = ["Imagen", "Nombre", "Modelo", "Serie", "Cantidad", "Sitio"]
    ws.append(headers)

    # Ajustar ancho de columnas
    ws.column_dimensions['A'].width = 20
    ws.column_dimensions['B'].width = 25
    ws.column_dimensions['C'].width = 18
    ws.column_dimensions['D'].width = 18
    ws.column_dimensions['E'].width = 12
    ws.column_dimensions['F'].width = 25

    # Ruta de la carpeta de imágenes
    ruta_imagenes = os.path.join(os.getcwd(), "static/images")

    for equipo in equipos:
        # Agregar información (dejando la primera celda vacía para la imagen)
        ws.append([None, equipo['nombre'], equipo['modelo'], equipo['serie'], equipo['cantidad'], equipo['sitio']])

        # Obtener la fila actual
        fila = ws.max_row

        # Insertar imagen
        imagen_path = os.path.join(ruta_imagenes, equipo['archivo'])
        if os.path.exists(imagen_path):
            img = XLImage(imagen_path)
            img.width = 80  # ajustar tamaño
            img.height = 80
            ws.add_image(img, f"A{fila}")

    # Guardar en memoria
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name="inventario_completo.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

if __name__ == "__main__":
    app.run()
