import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# ตั้งค่าหน้าเว็บ
# st.set_page_config(page_title="Dashboard", layout="wide")

# CSS Styling
st.markdown(
    """
    <style>
    /* Custom Styling */
    body {
        background-color: #f9fafb;
        font-family: 'Arial', sans-serif;
        color: #333333;
    }
    .stTitle {
        font-size: 28px;
        color: #2c3e50;
        font-weight: bold;
    }
    .metric-box {
        background: #ffffff !important;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ฟังก์ชันสำหรับดึงข้อมูลจาก PostgreSQL
@st.cache_data
def load_data():
    try:
        conn_str = "postgresql://smscdr:%23Ltc1qaz2wsx%40pg@172.28.27.50:5432/CDKPTL"
        engine = create_engine(conn_str)
        query = """
        SELECT operator_name, total_sub, active_sub, disable_sub, mbb, fbb, active_mbb, disable_mbb, active_fbb, disable_fbb, 
               total_fee_charge_mbb, total_fee_charge_fbb, total_fee_estimate, 
               total_collected_fee_mbb, total_collected_fee_fbb, total_collected_fee
        FROM gov.operator_detail where operator_name = 'ETL';
        """
        return pd.read_sql(query, engine)
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return pd.DataFrame()

# โหลดข้อมูล
st.title("Dashboard Monitor Fee Charge")
data = load_data()

# ตรวจสอบว่ามีข้อมูลหรือไม่
if not data.empty:
    # สรุปข้อมูล
    st.subheader("Operator ETL Subscribers", divider="gray")
    # col1, col2, col3, col4, col5, col6 = st.columns(6)
    # col1.metric("Total Subscribers", f"{data['total_sub'].sum():,}")
    # for col, operator in zip([col2, col3, col4, col5, col6], data['operator_name']):
    #     total_sub = data.loc[data['operator_name'] == operator, 'total_sub'].values[0]
    #     col.metric(operator, f"{total_sub:,}")

    # ใช้ CSS Styling เพื่อเพิ่มกรอบรอบ Metric Card
    st.markdown(
        """
        <style>
        .metric-box {
            background: #ffffff;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin: 10px;
        }
        .total-subscribers-box {
            background-color: #ffffff;
            padding: 20px;
           
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            text-align: center;
            font-size: 40px;
            font-weight: bold;
            margin: 20px 0;
        }
        .metric-card {
            background: #ffffff !important;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 15px;
            text-align: center;
        }
        .metric-card .stMetric {
            font-size: 18px;
            font-weight: bold;
            color: #2c3e50;
        
        }
        .metric-card .stMetricValue {
            font-size: 24px;
            font-weight: bold;
            color: #1a73e8;
          
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # แสดง Total Subscribers แบบ metric
    # total_subscribers = data['total_sub'].sum()
    # st.markdown(
    #     f"""
    #     <div class="total-subscribers-box">
    #         Total Subscribers: {total_subscribers:,}
    #     </div>
    #     """,
    #     unsafe_allow_html=True,
    # )
    # # สร้างกรอบรวมผู้ให้บริการทั้งหมด
    # for i in range(0, len(data), 5):  # สร้างทีละ 5 Operator
    #     cols = st.columns(5)
    #     for col, row in zip(cols, data.iloc[i:i + 5].itertuples()):
    #         with col:
    #             st.markdown(
    #                 f"""
    #                 <div class="metric-box">
    #                     <h5>{row.operator_name}</h3>
    #                     <p><b></b> <span style="font-size: 30px; font-weight: bold;">{row.total_sub:,}</span></p>
    #                 </div>
    #                 """,
    #                 unsafe_allow_html=True,
    #             )

    # cols = st.columns(6)
    # cols[0].metric("Total Subscribers", f"{data['total_sub'].sum():,}")
    # cols[1].metric("MBB", f"{data['mbb'].sum():,}")
    # cols[2].metric("FBB", f"{data['fbb'].sum():,}")
    # cols[3].metric("Active MBB", f"{data['active_mbb'].sum():,}")
    # cols[4].metric("Active FBB", f"{data['active_fbb'].sum():,}")
    # cols[5].metric("Disable MBB", f"{data['disable_mbb'].sum():,}")

    cols = st.columns(6)
    cols[0].markdown(
        """
        <div class="metric-card">
            <p>Total Subscribers</p>
            <h2>{:,}</h2>
        </div>
        """.format(data['total_sub'].sum()),
        unsafe_allow_html=True,
    )
    cols[1].markdown(
        """
        <div class="metric-card">
            <p>MBB</p>
            <h2>{:,}</h2>
        </div>
        """.format(data['mbb'].sum()),
        unsafe_allow_html=True,
    )
    cols[2].markdown(
        """
        <div class="metric-card">
            <p>FBB</p>
            <h2>{:,}</h2>
        </div>
        """.format(data['fbb'].sum()),
        unsafe_allow_html=True,
    )
    cols[3].markdown(
        """
        <div class="metric-card">
            <p>Active MBB</p>
            <h2>{:,}</h2>
        </div>
        """.format(data['active_mbb'].sum()),
        unsafe_allow_html=True,
    )
    cols[4].markdown(
        """
        <div class="metric-card">
            <p>Active FBB</p>
            <h2>{:,}</h2>
        </div>
        """.format(data['active_fbb'].sum()),
        unsafe_allow_html=True,
    )
    cols[5].markdown(
        """
        <div class="metric-card">
            <p>Disable MBB</p>
            <h2>{:,}</h2>
        </div>
        """.format(data['disable_mbb'].sum()),
        unsafe_allow_html=True,
    )

    # Fee Charge Summary
    st.subheader("Fee Charge", divider="gray")
    fee_col1, fee_col2 = st.columns(2)
    fee_col1.metric("Total Fee Estimate", f"{data['total_fee_estimate'].sum():,}")
    fee_col2.metric("Total Fee Collected", f"{data['total_collected_fee'].sum():,}")
   


    # st.subheader("Fee Charge")
    # fee_col1, fee_col2 = st.columns(2)

    # with fee_col1:
    #     # st.markdown('<div class="metric-box">', unsafe_allow_html=True)
    #     st.markdown("<h5>Total Fee Estimate</h3>", unsafe_allow_html=True)
    #     st.metric("", f"{data['total_fee_estimate'].sum():,}")
    #     st.markdown('</div>', unsafe_allow_html=True)

    # with fee_col2:
    #     # st.markdown('<div class="metric-box">', unsafe_allow_html=True)
    #     st.markdown("<h5>Total Fee Collected</h3>", unsafe_allow_html=True)
    #     st.metric("", f"{data['total_collected_fee'].sum():,}")
    #     st.markdown('</div>', unsafe_allow_html=True)

    # รายละเอียดค่าธรรมเนียม MBB และ FBB
    st.subheader("Details by Service Type", divider="gray")
    service_col1, service_col2, service_col3, service_col4 = st.columns(4)
    service_col1.metric("Total Fee Estimate MBB", f"{data['total_fee_charge_mbb'].sum():,}")
    service_col2.metric("Total Fee Collected MBB", f"{data['total_collected_fee_mbb'].sum():,}")
    service_col3.metric("Total Fee Estimate FBB", f"{data['total_fee_charge_fbb'].sum():,}")
    service_col4.metric("Total Fee Collected FBB", f"{data['total_collected_fee_fbb'].sum():,}")

    # Pie Charts
    st.subheader("Visualizations", divider="gray")
    pie_col1, pie_col2, pie_col3 = st.columns(3)

    # Total fee collected vs estimated
    fig1 = px.pie(
        values=[
            data['total_collected_fee'].sum(),
            data['total_fee_estimate'].sum() - data['total_collected_fee'].sum()
        ],
        names=["Collected", "Remaining"],
        title="Total Fee Collected"
    )
    pie_col1.plotly_chart(fig1)

    # Fee MBB collected vs estimated
    fig2 = px.pie(
        values=[
            data['total_collected_fee_mbb'].sum(),
            data['total_fee_charge_mbb'].sum() - data['total_collected_fee_mbb'].sum()
        ],
        names=["Collected MBB", "Remaining MBB"],
        title="MBB Fee Collected"
    )
    pie_col2.plotly_chart(fig2)

    # Fee FBB collected vs estimated
    fig3 = px.pie(
        values=[
            data['total_collected_fee_fbb'].sum(),
            data['total_fee_charge_fbb'].sum() - data['total_collected_fee_fbb'].sum()
        ],
        names=["Collected FBB", "Remaining FBB"],
        title="FBB Fee Collected"
    )
    pie_col3.plotly_chart(fig3)
else:
    st.warning("No data available to display.")
