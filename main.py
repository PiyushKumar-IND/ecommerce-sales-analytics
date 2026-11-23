
from flask import Flask, render_template_string
import pandas as pd
from pathlib import Path
import json

app = Flask(__name__)

# ==========================================
# 1. LOAD ECOMMERCE DATASET
# ==========================================

DATA_FILE = (
    Path(__file__).parent
    / "data"
    / "ecommerce_sales_analytics_5000.csv"
)

try:
    df = pd.read_csv(DATA_FILE)
    print("Dataset loaded successfully!")
except Exception as error:
    df = pd.DataFrame()
    print("Dataset loading error:", error)


# ==========================================
# 2. DETECT DATASET COLUMNS
# ==========================================

def find_column(possible_names):
    for column in df.columns:
        if column.strip().lower() in possible_names:
            return column
    return None


revenue_col = find_column({
    "revenue", "sales", "total sales", "amount",
    "total_amount", "order_amount", "purchase_amount"
})

category_col = find_column({
    "category", "product_category", "product category"
})

region_col = find_column({
    "region", "state", "location", "country"
})

date_col = find_column({
    "date", "order_date", "order date", "purchase_date"
})


# ==========================================
# 3. COMPLETE WEBSITE DESIGN
# ==========================================

HTML = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>SHOPLYTICS | Ecommerce Analytics</title>

    <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>

    <style>

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: Arial, sans-serif;
            background: #f5f7fb;
            color: #182230;
        }

        /* MAIN LAYOUT */

        .layout {
            display: flex;
            min-height: 100vh;
        }

        /* SIDEBAR */

        .sidebar {
            width: 245px;
            min-height: 100vh;
            background: #111827;
            color: white;
            padding: 28px 18px;
            flex-shrink: 0;
        }

        .brand {
            font-size: 24px;
            font-weight: 800;
            margin-bottom: 45px;
            padding-left: 8px;
        }

        .brand span {
            color: #38bdf8;
        }

        .nav-label {
            color: #94a3b8;
            font-size: 11px;
            letter-spacing: 1.5px;
            margin: 25px 10px 12px;
        }

        .nav-item {
            display: block;
            padding: 14px 12px;
            color: #cbd5e1;
            text-decoration: none;
            border-radius: 9px;
            margin-bottom: 7px;
            font-size: 14px;
            transition: 0.2s;
        }

        .nav-item:hover {
            background: #263449;
            color: white;
        }

        .nav-item.active {
            background: #2563eb;
            color: white;
        }

        /* MAIN CONTENT */

        .main {
            flex: 1;
            min-width: 0;
            padding: 30px;
        }

        .topbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 15px;
            margin-bottom: 30px;
        }

        .topbar h1 {
            font-size: 27px;
            margin-bottom: 8px;
        }

        .topbar p {
            color: #64748b;
            font-size: 14px;
        }

        .profile {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 30px;
            padding: 12px 18px;
            font-size: 13px;
        }

        /* SECTION TITLES */

        .section-title {
            font-size: 19px;
            margin: 25px 0 16px;
        }

        /* KPI CARDS */

        .cards {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 18px;
        }

        .card {
            background: white;
            padding: 23px;
            border-radius: 15px;
            border: 1px solid #edf0f5;
            box-shadow: 0 5px 20px rgba(15, 23, 42, 0.04);
            transition: 0.2s;
        }

        .card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 25px rgba(15, 23, 42, 0.08);
        }

        .card-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .card-icon {
            width: 45px;
            height: 45px;
            display: grid;
            place-items: center;
            border-radius: 12px;
            font-size: 22px;
        }

        .blue {
            background: #dbeafe;
        }

        .green {
            background: #dcfce7;
        }

        .purple {
            background: #f3e8ff;
        }

        .orange {
            background: #ffedd5;
        }

        .card h3 {
            font-size: 13px;
            font-weight: 500;
            color: #64748b;
            margin: 19px 0 9px;
        }

        .card h2 {
            font-size: 25px;
            color: #172033;
            overflow-wrap: anywhere;
        }

        /* CHARTS */

        .charts {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 20px;
        }

        .chart-card {
            background: white;
            border: 1px solid #edf0f5;
            border-radius: 15px;
            padding: 20px;
            min-width: 0;
            box-shadow: 0 5px 20px rgba(15, 23, 42, 0.04);
        }

        .chart-card h2 {
            font-size: 16px;
            margin-bottom: 7px;
        }

        .chart-card p {
            color: #94a3b8;
            font-size: 12px;
            margin-bottom: 10px;
        }

        .plot {
            width: 100%;
            height: 340px;
        }

        .wide {
            grid-column: 1 / -1;
        }

        /* DATA TABLE */

        .table-card {
            margin-top: 22px;
            background: white;
            border-radius: 15px;
            padding: 22px;
            border: 1px solid #edf0f5;
            overflow-x: auto;
        }

        .table-card h2 {
            font-size: 18px;
            margin-bottom: 8px;
        }

        .table-description {
            color: #94a3b8;
            font-size: 13px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
            margin-top: 18px;
        }

        th {
            background: #eff6ff;
            color: #475569;
            text-align: left;
        }

        th, td {
            padding: 13px;
            border-bottom: 1px solid #edf0f5;
            white-space: nowrap;
        }

        tr:hover td {
            background: #f8fafc;
        }

        /* ERROR MESSAGE */

        .notice {
            background: #fff7ed;
            color: #9a3412;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
        }

        /* FOOTER */

        footer {
            text-align: center;
            color: #94a3b8;
            padding: 28px;
            font-size: 12px;
        }

        /* RESPONSIVE DESIGN */

        @media (max-width: 1100px) {
            .cards {
                grid-template-columns: repeat(2, 1fr);
            }
        }

        @media (max-width: 750px) {

            .sidebar {
                width: 75px;
                padding: 20px 8px;
            }

            .brand {
                font-size: 13px;
                padding: 0;
                text-align: center;
            }

            .nav-label {
                display: none;
            }

            .nav-item {
                font-size: 0;
                text-align: center;
            }

            .nav-item::first-letter {
                font-size: 20px;
            }

            .main {
                padding: 18px;
            }

            .charts {
                grid-template-columns: 1fr;
            }

            .wide {
                grid-column: auto;
            }

            .topbar h1 {
                font-size: 21px;
            }
        }

        @media (max-width: 480px) {

            .cards {
                grid-template-columns: 1fr;
            }

            .profile {
                display: none;
            }
        }

    </style>
</head>

<body>

<div class="layout">

    <!-- SIDEBAR -->

    <aside class="sidebar">

        <div class="brand">
            SHOP<span>LYTICS.</span>
        </div>

        <div class="nav-label">MAIN MENU</div>

        <a href="#" class="nav-item active">
            ▦ Dashboard
        </a>

        <a href="#charts" class="nav-item">
            ◷ Analytics
        </a>

        <a href="#dataset" class="nav-item">
            ▤ Dataset
        </a>

        <div class="nav-label">PROJECT</div>

        <a href="#charts" class="nav-item">
            ◈ Reports
        </a>

    </aside>


    <!-- MAIN DASHBOARD -->

    <main class="main">

        <div class="topbar">

            <div>
                <h1>Dashboard Overview</h1>
                <p>Welcome to your ecommerce business analytics.</p>
            </div>

            <div class="profile">
                👤 Admin Dashboard
            </div>

        </div>


        {% if error %}
            <div class="notice">{{ error }}</div>
        {% endif %}


        <!-- KPI CARDS -->

        <h2 class="section-title">
            Business Performance
        </h2>

        <section class="cards">

            <div class="card">

                <div class="card-top">
                    <div class="card-icon blue">🛒</div>
                </div>

                <h3>Total Orders / Records</h3>
                <h2>{{ total_records }}</h2>

            </div>


            <div class="card">

                <div class="card-top">
                    <div class="card-icon green">💰</div>
                </div>

                <h3>Total Revenue</h3>
                <h2>{{ total_revenue }}</h2>

            </div>


            <div class="card">

                <div class="card-top">
                    <div class="card-icon purple">📊</div>
                </div>

                <h3>Average Revenue</h3>
                <h2>{{ average_revenue }}</h2>

            </div>


            <div class="card">

                <div class="card-top">
                    <div class="card-icon orange">✓</div>
                </div>

                <h3>Missing Values</h3>
                <h2>{{ missing_values }}</h2>

            </div>

        </section>


        <!-- CHARTS -->

        <h2 class="section-title" id="charts">
            Sales Analytics
        </h2>

        <section class="charts">

            <div class="chart-card">

                <h2>Revenue by Category</h2>

                <p>
                    Sales performance across product categories
                </p>

                <div id="categoryChart" class="plot"></div>

            </div>


            <div class="chart-card">

                <h2>Revenue by Region</h2>

                <p>
                    Regional revenue distribution
                </p>

                <div id="regionChart" class="plot"></div>

            </div>


            <div class="chart-card wide">

                <h2>Monthly Revenue Trend</h2>

                <p>
                    Track revenue performance over time
                </p>

                <div id="monthlyChart" class="plot"></div>

            </div>

        </section>


        <!-- DATASET TABLE -->

        <section class="table-card" id="dataset">

            <h2>📋 Dataset Overview</h2>

            <p class="table-description">
                Preview of your ecommerce sales records
            </p>

            {{ table | safe }}

        </section>


        <footer>
            SHOPLYTICS © 2026 | Ecommerce Sales Intelligence
        </footer>

    </main>

</div>


<!-- PLOTLY CHARTS -->

<script>

    const categoryData = {{ category_chart | safe }};
    const regionData = {{ region_chart | safe }};
    const monthlyData = {{ monthly_chart | safe }};

    const chartLayout = {
        autosize: true,
        paper_bgcolor: "white",
        plot_bgcolor: "white",

        font: {
            family: "Arial",
            color: "#64748b"
        },

        margin: {
            t: 15,
            r: 15,
            b: 55,
            l: 55
        }
    };


    function drawChart(id, data) {

        if (data && data.length > 0) {

            Plotly.newPlot(
                id,
                data,
                chartLayout,
                {
                    responsive: true,
                    displayModeBar: false
                }
            );

        } else {

            document.getElementById(id).innerHTML =
                "<p style='padding:20px;color:#64748b'>Chart data not available.</p>";

        }

    }


    drawChart("categoryChart", categoryData);
    drawChart("regionChart", regionData);
    drawChart("monthlyChart", monthlyData);

</script>

</body>
</html>
"""


# ==========================================
# 4. DASHBOARD ROUTE
# ==========================================

@app.route("/")
def dashboard():

    if df.empty:

        return render_template_string(
            HTML,
            error="Dataset could not be loaded. Check the CSV file.",
            total_records=0,
            total_revenue="N/A",
            average_revenue="N/A",
            missing_values=0,
            table="<p>No dataset available.</p>",
            category_chart="[]",
            region_chart="[]",
            monthly_chart="[]"
        )


    # BASIC STATISTICS

    total_records = len(df)

    missing_values = int(
        df.isnull().sum().sum()
    )

    total_revenue = "Column not found"
    average_revenue = "Column not found"

    if revenue_col:

        revenue = pd.to_numeric(
            df[revenue_col],
            errors="coerce"
        )

        total_revenue = f"{revenue.sum():,.2f}"

        average_revenue = f"{revenue.mean():,.2f}"


    # INITIALIZE CHARTS

    category_chart = []
    region_chart = []
    monthly_chart = []


    # REVENUE BY CATEGORY

    if revenue_col and category_col:

        temp = df.copy()

        temp[revenue_col] = pd.to_numeric(
            temp[revenue_col],
            errors="coerce"
        )

        grouped = (
            temp.groupby(category_col)[revenue_col]
            .sum()
            .reset_index()
        )

        category_chart = [{
            "type": "bar",

            "x": grouped[category_col].astype(str).tolist(),

            "y": grouped[revenue_col].fillna(0).tolist(),

            "marker": {
                "color": "#2563eb",
                "line": {
                    "color": "#1d4ed8",
                    "width": 1
                }
            }
        }]


    # REVENUE BY REGION

    if revenue_col and region_col:

        temp = df.copy()

        temp[revenue_col] = pd.to_numeric(
            temp[revenue_col],
            errors="coerce"
        )

        grouped = (
            temp.groupby(region_col)[revenue_col]
            .sum()
            .reset_index()
        )

        region_chart = [{
            "type": "pie",

            "labels": grouped[region_col].astype(str).tolist(),

            "values": grouped[revenue_col].fillna(0).tolist(),

            "hole": 0.4,

            "textinfo": "label+percent",

            "marker": {
                "line": {
                    "color": "white",
                    "width": 2
                }
            }
        }]


    # MONTHLY REVENUE TREND

    if revenue_col and date_col:

        temp = df.copy()

        temp[date_col] = pd.to_datetime(
            temp[date_col],
            errors="coerce"
        )

        temp[revenue_col] = pd.to_numeric(
            temp[revenue_col],
            errors="coerce"
        )

        temp = temp.dropna(
            subset=[date_col, revenue_col]
        )

        temp["Month"] = (
            temp[date_col]
            .dt.to_period("M")
            .astype(str)
        )

        grouped = (
            temp.groupby("Month")[revenue_col]
            .sum()
            .reset_index()
            .sort_values("Month")
        )

        monthly_chart = [{

            "type": "scatter",

            "mode": "lines+markers",

            "x": grouped["Month"].tolist(),

            "y": grouped[revenue_col].tolist(),

            "line": {
                "color": "#16a34a",
                "width": 3
            },

            "marker": {
                "size": 7
            }

        }]


    # DATASET PREVIEW

    table = df.head(10).to_html(
        classes="data-table",
        index=False,
        border=0
    )


    # WARNINGS

    error = None

    if not revenue_col:

        error = (
            "Revenue column was not detected. "
            "Please check your CSV column names."
        )


    # SEND DATA TO HTML

    return render_template_string(

        HTML,

        error=error,

        total_records=f"{total_records:,}",

        total_revenue=total_revenue,

        average_revenue=average_revenue,

        missing_values=f"{missing_values:,}",

        table=table,

        category_chart=json.dumps(category_chart),

        region_chart=json.dumps(region_chart),

        monthly_chart=json.dumps(monthly_chart)

    )


# ==========================================
# 5. RUN FLASK APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
