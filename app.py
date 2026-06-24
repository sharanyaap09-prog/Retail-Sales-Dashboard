import streamlit as st
import pandas as pd
import plotly.express as px

# ======================================
# PAGE CONFIGURATION
# ======================================

st.set_page_config(
    page_title="Retail Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Retail Sales Dashboard")

# ======================================
# LOAD DATA
# ======================================

df = pd.read_csv("retail_sales_cleaned.csv")

# Convert OrderDate to datetime
df["OrderDate"] = pd.to_datetime(df["OrderDate"])

# ======================================
# SIDEBAR FILTERS
# ======================================

st.sidebar.header("Filters")

# Date Range Filter

start_date = st.sidebar.date_input(
    "Start Date",
    value=df["OrderDate"].min().date()
)

end_date = st.sidebar.date_input(
    "End Date",
    value=df["OrderDate"].max().date()
)

# Region Filter

region = st.sidebar.multiselect(
    "Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

# Category Filter

category = st.sidebar.multiselect(
    "Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

# Segment Filter

segment = st.sidebar.multiselect(
    "Segment",
    options=df["Segment"].unique(),
    default=df["Segment"].unique()
)

# ======================================
# APPLY FILTERS
# ======================================

filtered_df = df[
    (df["OrderDate"].dt.date >= start_date) &
    (df["OrderDate"].dt.date <= end_date) &
    (df["Region"].isin(region)) &
    (df["Category"].isin(category)) &
    (df["Segment"].isin(segment))
]

# ======================================
# KPI CALCULATIONS
# ======================================

total_revenue = filtered_df["Sales"].sum()

total_profit = filtered_df["Profit"].sum()

total_orders = filtered_df["OrderID"].nunique()

aov = total_revenue / total_orders if total_orders > 0 else 0

# ======================================
# KPI CARDS
# ======================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Revenue", f"{total_revenue:,.0f}")

with col2:
    st.metric("Profit", f"{total_profit:,.0f}")

with col3:
    st.metric("AOV", f"{aov:,.0f}")

with col4:
    st.metric("Orders", f"{total_orders:,}")

st.markdown("---")
# ======================================
# CHARTS - 2 X 2 MATRIX
# ======================================

# ---------- Monthly Sales Trend ----------

monthly_sales = filtered_df.copy()

monthly_sales["YearMonth"] = (
    monthly_sales["OrderDate"]
    .dt.to_period("M")
    .astype(str)
)

monthly_sales = (
    monthly_sales
    .groupby("YearMonth")["Sales"]
    .sum()
    .reset_index()
)

fig1 = px.line(
    monthly_sales,
    x="YearMonth",
    y="Sales",
    markers=True,
    title="Monthly Sales Trend"
)

# ---------- Sales by Category ----------

category_sales = (
    filtered_df
    .groupby("Category")["Sales"]
    .sum()
    .reset_index()
)

fig2 = px.bar(
    category_sales,
    x="Category",
    y="Sales",
    title="Sales by Category",
    text_auto=True
)

# ---------- Sales by SubCategory ----------

subcategory_sales = (
    filtered_df
    .groupby("SubCategory")["Sales"]
    .sum()
    .reset_index()
    .sort_values("Sales", ascending=False)
    .head(10)
)

fig3 = px.bar(
    subcategory_sales,
    x="SubCategory",
    y="Sales",
    title="Top 10 SubCategories",
    text_auto=True
)

# ---------- Top 10 Customers ----------

top_customers = (
    filtered_df
    .groupby("CustomerName")["Sales"]
    .sum()
    .reset_index()
    .sort_values("Sales", ascending=False)
    .head(10)
)

fig4 = px.bar(
    top_customers,
    x="CustomerName",
    y="Sales",
    title="Top 10 Customers",
    text_auto=True
)

# ======================================
# FIRST ROW
# ======================================

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.plotly_chart(fig2, use_container_width=True)

# ======================================
# SECOND ROW
# ======================================

col3, col4 = st.columns(2)

with col3:
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# ======================================
# REGION COMPARISON
# ======================================

region_sales = (
    filtered_df
    .groupby("Region")["Sales"]
    .sum()
    .reset_index()
)

fig5 = px.bar(
    region_sales,
    x="Region",
    y="Sales",
    title="Region Comparison",
    text_auto=True
)

st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")
# ======================================
# DATA TABLE
# ======================================

st.subheader("Filtered Data")

st.dataframe(
    filtered_df,
    use_container_width=True
)