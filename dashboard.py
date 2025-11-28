import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# ----------------------------------------------------
# Load Dataset Safely
# ----------------------------------------------------
CSV_NAME = "Business_sales.csv"

if os.path.exists(CSV_NAME):
    df = pd.read_csv(CSV_NAME)
else:
    df = pd.DataFrame()

# ----------------------------------------------------
# Ensure Columns Exist
# ----------------------------------------------------
expected_cols = ["Product ID","Product Position","Promotion","Product Category",
                 "Seasonal","Sales Volume","brand","url","name","description",
                 "price","currency","terms","section","season","material","origin"]

for c in expected_cols:
    if c not in df.columns:
        df[c] = ""

df["Sales Volume"] = pd.to_numeric(df["Sales Volume"], errors="coerce").fillna(0)
df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0)

df_clean = df[(df["Sales Volume"] > 0) & (df["price"] > 0)].copy()
df_clean["Revenue"] = df_clean["Sales Volume"] * df_clean["price"]

# ----------------------------------------------------
# KPI Calculations
# ----------------------------------------------------
total_revenue = df_clean["Revenue"].sum()
total_units = df_clean["Sales Volume"].sum()
avg_price = df_clean["price"].mean()
unique_products = df_clean["Product ID"].nunique()

# ----------------------------------------------------
# Aggregations for Charts
# ----------------------------------------------------
def g(df, col):
    if col not in df.columns or df.empty:
        return pd.DataFrame()
    return df.groupby(col, as_index=False)["Sales Volume"].sum().sort_values("Sales Volume", ascending=False)

by_position = g(df_clean, "Product Position")
promo = g(df_clean, "Promotion")
by_season = g(df_clean, "season")
by_material = g(df_clean, "material")
by_origin = g(df_clean, "origin")
top10 = df_clean.groupby("name", as_index=False)["Sales Volume"].sum().sort_values("Sales Volume", ascending=False).head(10)

# ----------------------------------------------------
# Figures
# ----------------------------------------------------
def make_bar(df, x, y, title):
    if df.empty:
        return go.Figure()
    fig = px.bar(df, x=x, y=y, title=title)
    fig.update_layout(margin=dict(t=40, l=10, r=10, b=10))
    return fig

def make_hbar(df, x, y, title):
    if df.empty:
        return go.Figure()
    fig = px.bar(df, x=x, y=y, orientation="h", title=title)
    fig.update_layout(margin=dict(t=40, l=10, r=10, b=10))
    return fig

fig_season = make_bar(by_season, "season", "Sales Volume", "Sales by Season")
fig_price_vs = px.scatter(df_clean, x="price", y="Sales Volume", hover_name="name", title="Price vs Sales Volume") if not df_clean.empty else go.Figure()
fig_top10 = make_hbar(top10, "Sales Volume", "name", "Top 10 Products by Sales Volume")
fig_material = make_bar(by_material, "material", "Sales Volume", "Sales by Material")
fig_position = make_bar(by_position, "Product Position", "Sales Volume", "Sales by Product Position")
fig_promo = make_bar(promo, "Promotion", "Sales Volume", "Sales: Promotion vs No Promotion")
fig_origin = make_bar(by_origin, "origin", "Sales Volume", "Sales by Region / Origin")

# ----------------------------------------------------
# PNG icons (stored online — always load correctly)
# ----------------------------------------------------
ICON_REVENUE = "https://i.imgur.com/8Km9tLL.png"
ICON_UNITS = "https://i.imgur.com/sWJYqz0.png"
ICON_PRICE = "https://i.imgur.com/4YQZ8zC.png"
ICON_PRODUCTS = "https://i.imgur.com/AFaH7aV.png"

# ----------------------------------------------------
# App Layout
# ----------------------------------------------------
app = Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    dcc.Location(id="url", refresh=False),

    html.Div([
        html.A("Overview", href="/"),
        html.A("Details", href="/details", style={"marginLeft":"25px"}),
        html.A("Advanced", href="/advanced", style={"marginLeft":"25px"}),
        html.A("Insights", href="/insights", style={"marginLeft":"25px"}),
    ], style={"padding":"15px","fontSize":"18px","fontWeight":"600"}),

    html.Div(id="page-content", style={"padding":"20px"})
])

# ----------------------------------------------------
# Page Functions
# ----------------------------------------------------
def page_overview():
    kpis = html.Div([
        html.Div([
            html.Img(src=ICON_REVENUE, style={"height":"30px"}),
            html.Div(f"${total_revenue:,.2f}", style={"fontSize":"22px","fontWeight":"700"}),
            html.Div("Total Revenue", style={"color":"gray"})
        ], style=kpi_style),

        html.Div([
            html.Img(src=ICON_UNITS, style={"height":"30px"}),
            html.Div(f"{int(total_units):,}", style={"fontSize":"22px","fontWeight":"700"}),
            html.Div("Total Units", style={"color":"gray"})
        ], style=kpi_style),

        html.Div([
            html.Img(src=ICON_PRICE, style={"height":"30px"}),
            html.Div(f"${avg_price:,.2f}", style={"fontSize":"22px","fontWeight":"700"}),
            html.Div("Average Price", style={"color":"gray"})
        ], style=kpi_style),

        html.Div([
            html.Img(src=ICON_PRODUCTS, style={"height":"30px"}),
            html.Div(f"{unique_products}", style={"fontSize":"22px","fontWeight":"700"}),
            html.Div("Unique Products", style={"color":"gray"})
        ], style=kpi_style),

    ], style={"display":"flex","gap":"20px","marginBottom":"20px","flexWrap":"wrap"})

    charts = html.Div([
        html.Div(dcc.Graph(figure=fig_position), style=card),
        html.Div(dcc.Graph(figure=fig_promo), style=card),
        html.Div(dcc.Graph(figure=fig_origin), style=card),
    ])

    return html.Div([kpis, charts])

def page_details():
    return html.Div([
        html.Div(dcc.Graph(figure=fig_top10), style=card),
        html.Div(dcc.Graph(figure=fig_material), style=card),
    ])

def page_advanced():
    return html.Div([
        html.Div(dcc.Graph(figure=fig_season), style=card),
        html.Div(dcc.Graph(figure=fig_price_vs), style=card),
    ])

def page_insights():
    insights = [
        f"Most sales come from the '{by_position.iloc[0]['Product Position']}' position." if not by_position.empty else "",
        f"Top season: {by_season.iloc[0]['season']}" if not by_season.empty else "",
        f"Strongest region: {by_origin.iloc[0]['origin']}" if not by_origin.empty else "",
    ]

    recs = [
        "Increase placement in high-performing product positions.",
        "Review pricing strategy for high-volume items.",
        "Expand sourcing where performance is high.",
        "Boost seasonal campaigns based on strongest seasons."
    ]

    return html.Div([
        html.H3("Insights"),
        html.Ul([html.Li(i) for i in insights if i != ""]),
        html.Br(),
        html.H3("Recommendations"),
        html.Ul([html.Li(r) for r in recs]),
    ], style=card)

# ----------------------------------------------------
# Styles
# ----------------------------------------------------
kpi_style = {
    "background":"white",
    "padding":"15px",
    "borderRadius":"10px",
    "boxShadow":"0 2px 8px rgba(0,0,0,0.1)",
    "width":"200px",
    "textAlign":"center"
}

card = {
    "background":"white",
    "padding":"15px",
    "borderRadius":"10px",
    "boxShadow":"0 2px 8px rgba(0,0,0,0.1)",
    "marginBottom":"20px"
}

# ----------------------------------------------------
# Routing
# ----------------------------------------------------
@app.callback(Output("page-content", "children"),
              Input("url", "pathname"))
def change_page(path):
    if path == "/details":
        return page_details()
    if path == "/advanced":
        return page_advanced()
    if path == "/insights":
        return page_insights()
    return page_overview()

# ----------------------------------------------------
# Run
# ----------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)