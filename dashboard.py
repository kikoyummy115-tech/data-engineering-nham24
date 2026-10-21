import os
import streamlit as st
import pandas as pd
import psycopg
import plotly.express as px
from dotenv import load_dotenv

# Page setup
st.set_page_config(
    page_title="Nham24 Analytics Dashboard",
    page_icon="🛵",
    layout="wide",
)

load_dotenv()
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:na123@localhost:5432/datawarehouse"
)


# Cached database query helper
@st.cache_data(ttl=300)
def fetch_query(query: str) -> pd.DataFrame:
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            columns = [desc[0] for desc in cur.description]
            records = cur.fetchall()
            return pd.DataFrame(records, columns=columns)


# Load analytics datasets
try:
    df_kpi = fetch_query("""
        SELECT 
            COUNT(DISTINCT c.customer_id) AS total_customers,
            ROUND(AVG(c.lifetime_orders_count), 1) AS avg_orders,
            ROUND(AVG(c.points_balance), 0) AS avg_points,
            ROUND(
                COUNT(DISTINCT CASE WHEN p.payment_type = 'KHQR_DIRECT' THEN c.customer_id END) * 100.0 
                / NULLIF(COUNT(DISTINCT c.customer_id), 0), 1
            ) AS khqr_adoption_pct
        FROM customers c
        LEFT JOIN customer_payment_methods p ON c.customer_id = p.customer_id;
    """)

    df_districts = fetch_query("""
        SELECT 
            a.khan,
            COUNT(DISTINCT c.customer_id) AS total_customers,
            COUNT(a.address_id) AS total_delivery_points,
            ROUND(AVG(c.lifetime_orders_count), 1) AS avg_orders_per_customer
        FROM customers c
        JOIN customer_addresses a ON c.customer_id = a.customer_id
        WHERE a.city = 'Phnom Penh'
        GROUP BY a.khan
        ORDER BY total_delivery_points DESC;
    """)

    df_payments = fetch_query("""
        SELECT 
            payment_type,
            COALESCE(bank_name, 'Cash / Other') AS bank_name,
            COUNT(payment_method_id) AS total_methods
        FROM customer_payment_methods
        GROUP BY payment_type, bank_name
        ORDER BY total_methods DESC;
    """)

    df_loyalty = fetch_query("""
        SELECT 
            loyalty_tier,
            registered_channel,
            COUNT(*) AS customer_count,
            ROUND(AVG(lifetime_orders_count), 1) AS avg_orders
        FROM customers
        GROUP BY loyalty_tier, registered_channel
        ORDER BY customer_count DESC;
    """)

except Exception as e:
    st.error(f"Failed to connect to PostgreSQL: {e}")
    st.info("Check your DATABASE_URL in .env or make sure your PostgreSQL container is running.")
    st.stop()

# Header & Controls
st.title("🛵 Nham24 Customer & Delivery Analytics")
st.caption("Warehouse Layer: PostgreSQL | Transformed Dimensional Schema")

# Top KPI Metric Cards
kpi_row = df_kpi.iloc[0]
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Customers", f"{int(kpi_row['total_customers']):,}")
with col2:
    st.metric("Avg Orders / User", f"{kpi_row['avg_orders']}")
with col3:
    st.metric("Bakong / KHQR Share", f"{kpi_row['khqr_adoption_pct']}%")
with col4:
    st.metric("Avg Loyalty Points", f"{int(kpi_row['avg_points']):,}")

st.divider()

# Dashboard Tabs
tab_geo, tab_finance, tab_cohorts = st.tabs([
    "📍 Phnom Penh Logistics", 
    "💳 Payment Rails & Gateways", 
    "🏆 Loyalty & App Channels"
])

# Tab 1: Geographic Distribution
with tab_geo:
    st.subheader("Delivery Density by District (Khan)")
    col_chart, col_table = st.columns([3, 2])

    with col_chart:
        fig_geo = px.bar(
            df_districts,
            x="khan",
            y="total_delivery_points",
            color="avg_orders_per_customer",
            title="Active Delivery Hotspots vs. Order Frequency",
            labels={
                "khan": "District (Khan)",
                "total_delivery_points": "Total Drop-off Points",
                "avg_orders_per_customer": "Avg Orders"
            },
            color_continuous_scale="Blues",
        )
        st.plotly_chart(fig_geo, use_container_width=True)

    with col_table:
        st.write("##### District Logistics Summary")
        st.dataframe(df_districts, use_container_width=True, hide_index=True)

# Tab 2: Payments Breakdown
with tab_finance:
    st.subheader("Customer Payment Rail Adoption")
    col_pie, col_bar = st.columns(2)

    with col_pie:
        fig_pay_type = px.pie(
            df_payments,
            names="payment_type",
            values="total_methods",
            hole=0.4,
            title="Payment Method Types (KHQR vs COD vs Cards)",
        )
        st.plotly_chart(fig_pay_type, use_container_width=True)

    with col_bar:
        fig_banks = px.bar(
            df_payments[df_payments["bank_name"] != "Cash / Other"],
            x="bank_name",
            y="total_methods",
            title="Top Partner Banks (ABA, ACLEDA, Wing)",
            labels={"bank_name": "Bank", "total_methods": "Linked Accounts"},
            color="bank_name",
        )
        st.plotly_chart(fig_banks, use_container_width=True)

# Tab 3: Customer Segments
with tab_cohorts:
    st.subheader("Customer Tiers vs Acquisition Channel")
    col_tier, col_scatter = st.columns(2)

    with col_tier:
        fig_tier = px.bar(
            df_loyalty,
            x="loyalty_tier",
            y="customer_count",
            color="registered_channel",
            barmode="group",
            title="Customer Base by Loyalty Tier & OS Platform",
            category_orders={"loyalty_tier": ["Bronze", "Silver", "Gold", "Platinum"]},
        )
        st.plotly_chart(fig_tier, use_container_width=True)

    with col_scatter:
        fig_bubble = px.scatter(
            df_loyalty,
            x="customer_count",
            y="avg_orders",
            size="customer_count",
            color="loyalty_tier",
            hover_name="registered_channel",
            title="Order Frequency vs Segment Volume",
            labels={"customer_count": "Users in Segment", "avg_orders": "Avg Orders"},
        )
        st.plotly_chart(fig_bubble, use_container_width=True)