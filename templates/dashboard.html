{% extends "base.html" %}
{% block content %}

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<div class="dashboard">

    <!-- SIDEBAR -->
    <aside class="sidebar">
        <h3>📊 Dashboard</h3>

        <a href="/dashboard" class="btn">Todos</a>

        {% for m in meses_disponibles %}
            <a href="/dashboard?mes={{ m.valor }}"
               class="btn {% if mes == m.valor %}active{% endif %}">
                {{ m.valor }}
            </a>
        {% endfor %}
    </aside>

    <!-- CONTENIDO -->
    <main>

        <!-- KPIs -->
        <div class="kpis">
            <div class="kpi">Ingresos<br><b>{{ total_ingresos | money }}</b></div>
            <div class="kpi">Costos<br><b>{{ total_costos | money }}</b></div>
            <div class="kpi">Utilidad<br><b>{{ utilidad | money }}</b></div>
            <div class="kpi">Margen<br><b>{{ margen }}%</b></div>
        </div>

        <!-- GRAFICAS -->
        <div class="charts">
            <div class="box">
                <canvas id="barras"></canvas>
            </div>
            <div class="box">
                <canvas id="dona"></canvas>
            </div>
        </div>

        <!-- VENTAS DIA -->
        <div class="box">
            <h4>Ventas por día</h4>
            <table>
                <tr><th>Día</th><th>Pedidos</th><th>Total</th><th>Neto</th></tr>
                {% for v in ventas_dia %}
                <tr>
                    <td>{{ v.dia }}</td>
                    <td>{{ v.pedidos }}</td>
                    <td>{{ v.total | money }}</td>
                    <td>{{ v.neto | money }}</td>
                </tr>
                {% endfor %}
            </table>
        </div>

        <!-- TOP PRODUCTOS -->
        <div class="box">
            <h4>Top productos</h4>
            <table>
                <tr><th>Producto</th><th>Cantidad</th><th>Ingreso</th></tr>
                {% for p in top_productos %}
                <tr>
                    <td>{{ p.nombre }}</td>
                    <td>{{ p.cantidad }}</td>
                    <td>{{ p.ingreso | money }}</td>
                </tr>
                {% endfor %}
            </table>
        </div>

    </main>
</div>

<script>
new Chart(document.getElementById("barras"),{
    type:"bar",
    data:{
        labels:{{ ingresos|map(attribute="mes")|list|tojson }},
        datasets:[
            {label:"Ingresos",data:{{ ingresos|map(attribute="total")|list|tojson }},backgroundColor:"#22c55e"},
            {label:"Costos",data:{{ costos|map(attribute="costo")|list|tojson }},backgroundColor:"#ef4444"}
        ]
    },
    options:{maintainAspectRatio:false}
});

new Chart(document.getElementById("dona"),{
    type:"doughnut",
    data:{
        labels:{{ costos_tipo|map(attribute="tipo_costo")|list|tojson }},
        datasets:[{
            data:{{ costos_tipo|map(attribute="total")|list|tojson }},
            backgroundColor:["#f59e0b","#6366f1","#10b981","#ef4444"]
        }]
    },
    options:{maintainAspectRatio:false}
});
</script>

<style>
.dashboard{display:grid;grid-template-columns:200px 1fr;height:100vh}
.sidebar{background:#1f2937;color:#fff;padding:20px}
.btn{display:block;margin-bottom:8px;padding:8px;background:#f59e0b;color:#fff;border-radius:6px;text-align:center;text-decoration:none}
.btn.active{background:#ea580c}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:15px;margin:20px}
.kpi{background:#fff;padding:15px;border-radius:8px}
.charts{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin:20px}
.box{background:#fff;padding:15px;border-radius:8px;height:260px}
canvas{width:100%!important;height:100%!important}
table{width:100%;margin-top:8px}
th{background:#111;color:#fff;padding:6px}
td{padding:6px}
</style>

{% endblock %}
