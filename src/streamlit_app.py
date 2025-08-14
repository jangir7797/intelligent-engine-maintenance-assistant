"""
Streamlit dashboard for the Intelligent Engine Maintenance Assistant.
"""
import sys
import os
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.config import settings
from src.utils.logging_config import setup_logging, get_logger
from src.rag_pipeline.pipeline import RAGPipeline, VectorStore
from src.data_processing.document_loader import DocumentProcessor

# Setup logging
setup_logging("INFO")
logger = get_logger(__name__)

# Page configuration
st.set_page_config(
    page_title="Intelligent Engine Maintenance Assistant",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 0.3rem solid #1f77b4;
    }
    .source-box {
        background-color: #f9f9f9;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #ddd;
        margin: 0.5rem 0;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def initialize_rag_pipeline():
    """Initialize the RAG pipeline (cached for performance)."""
    try:
        vector_store = VectorStore()
        rag_pipeline = RAGPipeline(vector_store=vector_store)
        return rag_pipeline
    except Exception as e:
        st.error(f"Failed to initialize RAG pipeline: {e}")
        st.error("Please make sure you have:")
        st.error("1. Added your Google AI Studio API key to .env file")
        st.error("2. Run 'python initialize_db.py' to set up the database")
        return None


@st.cache_data
def load_synthetic_data():
    """Load synthetic data for visualizations."""
    try:
        # Load maintenance logs
        maintenance_path = Path("synthetic_maintenance_logs.csv")
        fleet_path = Path("synthetic_fleet_info.csv")
        obd_path = Path("synthetic_obd_codes.csv")

        maintenance_df = pd.read_csv(maintenance_path) if maintenance_path.exists() else pd.DataFrame()
        fleet_df = pd.read_csv(fleet_path) if fleet_path.exists() else pd.DataFrame()
        obd_df = pd.read_csv(obd_path) if obd_path.exists() else pd.DataFrame()

        return maintenance_df, fleet_df, obd_df
    except Exception as e:
        st.error(f"Error loading synthetic data: {e}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()


def create_cost_analysis_chart(maintenance_df):
    """Create cost analysis visualization."""
    if maintenance_df.empty:
        st.warning("No maintenance data available for cost analysis.")
        return

    # Calculate total costs
    maintenance_df['total_cost'] = maintenance_df['parts_cost'] + maintenance_df['labor_cost']

    # Monthly cost analysis
    maintenance_df['date'] = pd.to_datetime(maintenance_df['date'])
    maintenance_df['month'] = maintenance_df['date'].dt.to_period('M')

    monthly_costs = maintenance_df.groupby('month')['total_cost'].sum().reset_index()
    monthly_costs['month'] = monthly_costs['month'].astype(str)

    fig = px.line(
        monthly_costs, 
        x='month', 
        y='total_cost',
        title='Monthly Maintenance Costs Trend',
        labels={'total_cost': 'Total Cost ($)', 'month': 'Month'}
    )

    fig.update_layout(
        xaxis_tickangle=-45,
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)


def create_fleet_health_dashboard(maintenance_df, fleet_df):
    """Create fleet health overview."""
    if maintenance_df.empty or fleet_df.empty:
        st.warning("Insufficient data for fleet health dashboard.")
        return

    col1, col2 = st.columns(2)

    with col1:
        # Vehicle status distribution
        status_counts = fleet_df['status'].value_counts()
        fig_status = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title='Fleet Status Distribution'
        )
        st.plotly_chart(fig_status, use_container_width=True)

    with col2:
        # Maintenance by category
        category_costs = maintenance_df.groupby('service_category')['parts_cost'].sum().reset_index()
        fig_category = px.bar(
            category_costs,
            x='service_category',
            y='parts_cost',
            title='Maintenance Costs by Category'
        )
        fig_category.update_xaxis(tickangle=-45)
        st.plotly_chart(fig_category, use_container_width=True)
