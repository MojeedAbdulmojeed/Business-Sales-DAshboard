Business Sales Analytics Dashboard (Python + Dash)

A fully interactive, multi-page Business Sales Analytics Dashboard built using Python, Dash, and Plotly.
This project analyzes product performance, customer behavior, pricing impact, and sales patterns across several dimensions to deliver clear insights and actionable recommendations.

The dashboard contains 3 main pages:

Page 1-Overview

High-level business performance metrics with KPIs:

Total Sales Volume

Total Revenue

Total Products

Average Price

Includes:

Horizontal KPI cards

Progress indicators

Sparkline micro-trends

SVG/PNG Icons for visual clarity

— Sales Insights

Interactive charts showing:

Sales by Season

Price vs Sales Volume

Top 10 Products by Sales Volume

Sales by Material

Sales by Product Position

Sales: Promotion vs No Promotion

Sales by Region / Origin

Fully interactive with hover, zoom, and filters.

Page 3 — Insights & Recommendations

A written breakdown of:

Why key trends happened

What the trends mean for the business

What actions should be taken next

Designed to support decision-making, especially for retail, inventory optimization, and pricing strategy.

Tech Stack

Python

Dash

Plotly

Pandas

HTML/CSS

Bootstrap Layout (Dash Components)

Project Files
File	Description
dashboard.py	Main Dash dashboard app
Business_sales.csv	Dataset used
README.md	Project documentation
How to Run the Dashboard

Clone the repository

git clone https://github.com/yourusername/BusinessDashboard.git


Install dependencies

pip install -r requirements.txt


Run the dashboard

python dashboard.py


Open in your browser:

http://127.0.0.1:8050

Key Insights

Seasonality drives sales, with certain seasons generating higher volume.

Promotions significantly increase sales, showing strong price sensitivity.

Material type impacts demand, suggesting customer preference trends.

Product position affects visibility, supporting better store layout planning.

Top 10 products dominate sales, showing clear core revenue drivers.

Recommendations

✔ Improve stock allocation for high-demand seasons
✔ Expand product variations in high-selling material categories
✔ Increase promotional strategies for slow-moving items
✔ Optimize store/aisle positioning to increase visibility
✔ Prioritize top-performing products in marketing and display
