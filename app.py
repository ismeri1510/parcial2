from flask import Flask, render_template, request, redirect, url_for
from db import get_connection
import psycopg2.extras

app = Flask(__name__)


@app.route("/")
def inicio():
    conn = get_connection()

    cur = conn.cursor(
        cursor_factory=psycopg2.extras.RealDictCursor
    )

    cur.execute("SELECT * FROM productos ORDER BY id DESC")

    productos = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "index.html",
        productos=productos
    )

@app.route("/productos/nuevo", methods=["GET", "POST"])
def nuevo_producto():

    if request.method == "POST":

        codigo = request.form["codigo"]
        nombre = request.form["nombre"]
        categoria = request.form["categoria"]
        precio = request.form["precio"]
        existencia = request.form["existencia"]
        activo = "activo" in request.form

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO productos
            (codigo, nombre, categoria, precio, existencia, activo)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                codigo,
                nombre,
                categoria,
                precio,
                existencia,
                activo
            )
        )

        conn.commit()

        cur.close()
        conn.close()

        return redirect(url_for("inicio"))

    return render_template("nuevo_producto.html")

@app.route("/productos/editar/<int:id>", methods=["GET", "POST"])
def editar_producto(id):

    conn = get_connection()
    cur = conn.cursor(
        cursor_factory=psycopg2.extras.RealDictCursor
    )

    if request.method == "POST":

        codigo = request.form["codigo"]
        nombre = request.form["nombre"]
        categoria = request.form["categoria"]
        precio = request.form["precio"]
        existencia = request.form["existencia"]
        activo = "activo" in request.form

        cur.execute(
            """
            UPDATE productos
            SET codigo = %s,
                nombre = %s,
                categoria = %s,
                precio = %s,
                existencia = %s,
                activo = %s
            WHERE id = %s
            """,
            (
                codigo,
                nombre,
                categoria,
                precio,
                existencia,
                activo,
                id
            )
        )

        conn.commit()

        cur.close()
        conn.close()

        return redirect(url_for("inicio"))

    cur.execute(
        "SELECT * FROM productos WHERE id = %s",
        (id,)
    )

    producto = cur.fetchone()

    cur.close()
    conn.close()

    return render_template(
        "editar_producto.html",
        producto=producto
    )

@app.route("/productos/eliminar/<int:id>", methods=["POST"])
def eliminar_producto(id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM productos WHERE id = %s",
        (id,)
    )

    conn.commit()

    cur.close()
    conn.close()

    return redirect(url_for("inicio"))


if __name__ == "__main__":
    app.run(debug=True)