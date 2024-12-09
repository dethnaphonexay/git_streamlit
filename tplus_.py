import streamlit as st
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

# st.set_page_config(page_title="Dashboard", layout="wide")
# ฟังก์ชันสำหรับดึงข้อมูลจาก PostgreSQL
@st.cache_data
def load_data():
    conn_str = "postgresql://smscdr:%23Ltc1qaz2wsx%40pg@172.28.27.50:5432/CDKPTL"
    engine = create_engine(conn_str)
    query = """
    SELECT operator_name, total_sub, active_sub, disable_sub, mbb, fbb, active_mbb, disable_mbb, active_fbb, disable_fbb, 
           total_fee_charge_mbb, total_fee_charge_fbb, total_fee_estimate, 
           total_collected_fee_mbb, total_collected_fee_fbb, total_collected_fee
    FROM gov.operator_detail;
    """
    return pd.read_sql(query, engine)

# โหลดข้อมูล
st.title("Dashboard Monitor Fee Charge")
data = load_data()

# สรุปข้อมูล
st.subheader("Operator Total Subscribers")
col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("Total Subscribers", f"{data['total_sub'].sum():,}")
for col, operator in zip([col2, col3, col4, col5, col6], data['operator_name']):
    total_sub = data.loc[data['operator_name'] == operator, 'total_sub'].values[0]
    col.metric(operator, f"{total_sub:,}")

# Fee Charge Summary
st.subheader("Fee Charge")
fee_col1, fee_col2 = st.columns(2)
fee_col1.metric("Total Fee Estimate", f"{data['total_fee_estimate'].sum():,}")
fee_col2.metric("Total Fee Collected", f"{data['total_collected_fee'].sum():,}")

# รายละเอียดค่าธรรมเนียม MBB และ FBB
st.subheader("Details by Service Type")
service_col1, service_col2, service_col3, service_col4 = st.columns(4)
service_col1.metric("Total Fee Estimate MBB", f"{data['total_fee_charge_mbb'].sum():,}")
service_col2.metric("Total Fee Collected MBB", f"{data['total_collected_fee_mbb'].sum():,}")
service_col3.metric("Total Fee Estimate FBB", f"{data['total_fee_charge_fbb'].sum():,}")
service_col4.metric("Total Fee Collected FBB", f"{data['total_collected_fee_fbb'].sum():,}")

# Pie Charts
import plotly.express as px

st.subheader("Visualizations")
pie_col1, pie_col2, pie_col3 = st.columns(3)

# Total fee collected vs estimated
fig1 = px.pie(values=[data['total_collected_fee'].sum(), data['total_fee_estimate'].sum() - data['total_collected_fee'].sum()],
              names=["Collected", "Remaining"],
              title="Total Fee Collected")
pie_col1.plotly_chart(fig1)

# Fee MBB collected vs estimated
fig2 = px.pie(values=[data['total_collected_fee_mbb'].sum(), data['total_fee_charge_mbb'].sum() - data['total_collected_fee_mbb'].sum()],
              names=["Collected MBB", "Remaining MBB"],
              title="MBB Fee Collected")
pie_col2.plotly_chart(fig2)

# Fee FBB collected vs estimated
fig3 = px.pie(values=[data['total_collected_fee_fbb'].sum(), data['total_fee_charge_fbb'].sum() - data['total_collected_fee_fbb'].sum()],
              names=["Collected FBB", "Remaining FBB"],
              title="FBB Fee Collected")
pie_col3.plotly_chart(fig3)
