import streamlit as st
import pandas as pd
import plotly.express as px

from src.ingest.load_transactions import load_transactions
from src.ingest.load_cpi_wide import load_cpi_wide
from src.core.pie import build_cpi_panel, compute_personal_inflation
from src.core.weights import monthly_category_weights

st.set_page_config(page_title="Personal Inflation Estimator", layout="wide", page_icon="🥧")

@st.cache_data
def load_cpi_data():
    cpi_shelter = load_cpi_wide("data/raw/cpi_shelter.csv")
    cpi_food = load_cpi_wide("data/raw/cpi_food_home.csv")
    cpi_transport = load_cpi_wide("data/raw/cpi_transport.csv")
    cpi_energy = load_cpi_wide("data/raw/cpi_energy.csv")

    cpi_panel = build_cpi_panel({
        "housing": cpi_shelter,
        "groceries": cpi_food,
        "transport": cpi_transport,
        "energy": cpi_energy,
    })
    return cpi_panel

@st.cache_data
def load_person_data(person_id: str):
    transactions = load_transactions(f"data/mock/transactions_person_{person_id.lower()}.csv")
    return transactions

st.title("🥧 Personal Inflation Estimator (PIE)")
st.markdown("Analyze customized inflation metrics based on personal transaction history and CPI data.")

# Sidebar Controls
st.sidebar.header("Controls")
person_choice = st.sidebar.selectbox("Select Persona", ["Person A", "Person B"])
person_id = "a" if person_choice == "Person A" else "b"

cpi_panel = load_cpi_data()

try:
    transactions = load_person_data(person_id)
except Exception as e:
    st.error(f"Failed to load data for {person_choice}.")
    st.stop()

# Compute data
inflation_series = compute_personal_inflation(transactions, cpi_panel)
weights_df = monthly_category_weights(transactions)

# Layout
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"Monthly Inflation Rate ({person_choice})")
    
    # Prepare data for plotting
    infl_df = inflation_series.reset_index()
    infl_df.columns = ['Month', 'Inflation']
    infl_df['Inflation %'] = infl_df['Inflation'] * 100
    
    # Line chart using Plotly
    fig_line = px.line(
        infl_df, x='Month', y='Inflation %', 
        markers=True, 
        title="Personal Inflation over Time",
        template="plotly_dark",
        color_discrete_sequence=['#60a5fa']
    )
    fig_line.update_layout(hovermode="x unified")
    st.plotly_chart(fig_line, use_container_width=True)

with col2:
    st.subheader("Latest Spending Weights")
    
    # Get latest month weights
    latest_month = weights_df["month"].max()
    latest_weights = weights_df[weights_df["month"] == latest_month]
    
    # Pie chart using Plotly
    fig_pie = px.pie(
        latest_weights, 
        values='weight', 
        names='category', 
        title=f"Category Breakdown (As of {latest_month.strftime('%b %Y')})",
        template="plotly_dark",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

st.divider()

# Show raw data option
with st.expander("View Raw Data"):
    st.dataframe(infl_df.tail(12).style.format({"Inflation %": "{:.2f}%", "Inflation": "{:.4f}"}))
