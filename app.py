from flask import Flask, render_template, request, redirect, url_for, flash
from db import get_connection
from decimal import Decimal

app = Flask(__name__)
app.secret_key = "super_secret_key"


# ================= FILTRO MONEDA =================
@app.template_filter("money")
def money(value):
    try:
        return "${:,.2f}".format(float(value))
    except:
        return value


# ================= HOME =================
@app.route("/")
def index():
    return redirect(url_for("dashboard"))


# ================= NUEVO PEDIDO =================
@app.route("/nuevo_pedido", methods=["GET", "POST"])
def nuevo_pedido():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM productos WHERE activo = 1 ORDER BY categoria, nombre")
            productos = cursor.fetchall()

            cursor.execute("SELECT * FROM salsas")
            salsas = cursor.fetchall()

            cursor.execute("SELECT * FROM proteinas")
            proteinas = cursor.fetchall()

            if request.method == "POST":
                origen = request.form["origen"]
                mesero = request.form["mesero"]
                metodo_pago = request.form["metodo_pago"]
                monto_uber = Decimal(request.form.get("monto_uber", 0) or 0)

                productos_ids = request.form.getlist("producto_id")
                cantidades = request.form.getlist("cantidad")

                total = Decimal("0")
                items = []

                for i, prod_id in enumerate(productos_ids):
                    if not prod_id:
                        continue

                    cant = int(cantidades[i] or 0)
                    if cant <= 0:
                        continue

                    cursor.execute("SELECT precio FROM productos WHERE id = %s", (prod_id,))
                    precio = Decimal(cursor.fetchone()["precio"])

                    subtotal = precio * cant
                    total += subtotal

                    items.append((prod_id, cant, precio, subtotal))

                neto = total + monto_uber

                cursor.execute("""
                    INSERT INTO pedidos (fecha, origen, mesero, metodo_pago, total, monto_uber, neto)
                    VALUES (NOW(), %s, %s, %s, %s, %s, %s)
                """, (origen, mesero, metodo_pago, total, monto_uber, neto))

                pedido_id = cursor.lastrowid

                for it in items:
                    cursor.execute("""
                        INSERT INTO pedido_items
                        (pedido_id, producto_id, cantidad, precio_unitario, subtotal)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (pedido_id, it[0], it[1], it[2], it[3]))

                conn.commit()
                flash(f"✅ Pedido #{pedido_id} registrado", "success")
                return redirect(url_for("nuevo_pedido"))

    finally:
        conn.close()

    return render_template("nuevo_pedido.html", productos=productos, salsas=salsas, proteinas=proteinas)


# ================= DASHBOARD =================
@app.route("/dashboard")
def dashboard():
    mes = request.args.get("mes")

    conn = get_connection()
    try:
        with conn.cursor() as cursor:

            # -------- MESES DISPONIBLES --------
            cursor.execute("""
                SELECT DISTINCT DATE_FORMAT(fecha, '%Y-%m') AS valor
                FROM pedidos
                ORDER BY valor DESC
            """)
            meses_disponibles = cursor.fetchall()

            filtro = ""
            params = ()

            if mes:
                filtro = "WHERE DATE_FORMAT(fecha, '%Y-%m') = %s"
                params = (mes,)

            # -------- INGRESOS --------
            cursor.execute(f"""
                SELECT DATE_FORMAT(fecha, '%Y-%m') mes, SUM(total) total
                FROM pedidos
                {filtro}
                GROUP BY mes
                ORDER BY mes
            """, params)
            ingresos = cursor.fetchall()

            # -------- COSTOS --------
            cursor.execute(f"""
                SELECT DATE_FORMAT(fecha, '%Y-%m') mes, SUM(costo) costo
                FROM insumos_compras
                {filtro}
                GROUP BY mes
                ORDER BY mes
            """, params)
            costos = cursor.fetchall()

            # -------- COSTOS POR TIPO --------
            cursor.execute(f"""
                SELECT tipo_costo, SUM(costo) total
                FROM insumos_compras
                {filtro}
                GROUP BY tipo_costo
            """, params)
            costos_tipo = cursor.fetchall()

            # -------- VENTAS POR DIA --------
            cursor.execute(f"""
                SELECT DATE(fecha) dia,
                       COUNT(*) pedidos,
                       SUM(total) total,
                       SUM(neto) neto
                FROM pedidos
                {filtro}
                GROUP BY DATE(fecha)
                ORDER BY dia DESC
                LIMIT 15
            """, params)
            ventas_dia = cursor.fetchall()

            # -------- TOP PRODUCTOS --------
            cursor.execute(f"""
                SELECT p.nombre,
                       SUM(pi.cantidad) cantidad,
                       SUM(pi.subtotal) ingreso
                FROM pedido_items pi
                JOIN productos p ON p.id = pi.producto_id
                JOIN pedidos pe ON pe.id = pi.pedido_id
                {filtro.replace("fecha", "pe.fecha")}
                GROUP BY p.id
                ORDER BY ingreso DESC
                LIMIT 10
            """, params)
            top_productos = cursor.fetchall()

            total_ingresos = sum(i["total"] for i in ingresos if i["total"])
            total_costos = sum(c["costo"] for c in costos if c["costo"])
            utilidad = total_ingresos - total_costos
            margen = round((utilidad / total_ingresos * 100), 2) if total_ingresos else 0

    finally:
        conn.close()

    return render_template(
        "dashboard.html",
        ingresos=ingresos,
        costos=costos,
        costos_tipo=costos_tipo,
        ventas_dia=ventas_dia,
        top_productos=top_productos,
        meses_disponibles=meses_disponibles,
        mes=mes,
        total_ingresos=total_ingresos,
        total_costos=total_costos,
        utilidad=utilidad,
        margen=margen
    )


# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)
