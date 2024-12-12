import streamlit as st
import pandas as pd
# from sqlalchemy import create_engine
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
# @st.cache_data
# def load_data():
#     try:
#         conn_str = "postgresql://smscdr:%23Ltc1qaz2wsx%40pg@172.28.27.50:5432/CDKPTL"
#         engine = create_engine(conn_str)
#         query = """
#         SELECT operator_name, total_sub, active_sub, disable_sub, mbb, fbb, active_mbb, disable_mbb, active_fbb, disable_fbb, 
#                total_fee_charge_mbb, total_fee_charge_fbb, total_fee_estimate, 
#                total_collected_fee_mbb, total_collected_fee_fbb, total_collected_fee
#         FROM gov.operator_detail;
#         """
#         return pd.read_sql(query, engine)
#     except Exception as e:
#         st.error(f"Error connecting to database: {e}")
#         return pd.DataFrame()

# โหลดข้อมูล
st.title("Dashboard Monitor Fee Charge")

# Define the data
datas = {
    "operator_name": ["LTC", "ETL", "TPLUS", "UNITEL", "BEST"],
    "total_sub": [2100356, 1087876, 1210692, 2325848, 807054],
    "active_sub": [1850000, 985420, 1005486, 1956896, 752365],
    "disable_sub": [250356, 102456, 205206, 368952, 54689],
    "mbb": [1943527, 1027682, 1210692, 2118235, 795863],
    "fbb": [156829, 60194, None, 207613, 11191],
    "active_mbb": [1713725, 940278, 1005486, 1765155, 743217],
    "disable_mbb": [229802, 87404, 205206, 353080, 52646],
    "active_fbb": [136275, 45142, None, 191741, 9148],
    "disable_fbb": [20554, 15052, None, 15872, 2043],
    "total_fee_charge_mbb": [5141175000, 2820834000, 3016458000, 5295465000, 2229651000],
    "total_fee_charge_fbb": [681375000, 225710000, None, 958705000, 45740000],
    "total_fee_estimate": [5822550000, 3046544000, 3016458000, 6254170000, 2275391000],
    "total_collected_fee_mbb": [3907293000, 2256667200, 2714812200, 4501145250, 2162761470],
    "total_collected_fee_fbb": [647306250, 196367700, None, 853247450, 43453000],
    "total_collected_fee": [4554599250, 2453034900, 2714812200, 5354392700, 2206214470],
}

# Create the DataFrame
data = pd.DataFrame(datas)



# ตรวจสอบว่ามีข้อมูลหรือไม่
if not data.empty:
    # สรุปข้อมูล
    st.subheader("Operator Total Subscribers", divider="gray")
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
            background-color: #f8f9f9;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin: 10px;
        }
        .total-subscribers-box {
            background-color: #f8f9f9;
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
    total_subscribers = data['total_sub'].sum()
    st.markdown(
        f"""
        <div class="total-subscribers-box">
            Total Subscribers: {total_subscribers:,}
        </div>
        """,
        unsafe_allow_html=True,
    )
    # สร้างกรอบรวมผู้ให้บริการทั้งหมด
    for i in range(0, len(data), 5):  # สร้างทีละ 5 Operator
        cols = st.columns(5)
        for col, row in zip(cols, data.iloc[i:i + 5].itertuples()):
            with col:
                st.markdown(
                    f"""
                    <div class="metric-box">
                        <h5>{row.operator_name}</h5>
                        <p><b></b> <span style="font-size: 30px; font-weight: bold;">{row.total_sub:,}</span></p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # Fee Charge Summary
    total_fee_estimate = data['total_fee_estimate'].sum()
    total_collected_fee = data['total_collected_fee'].sum()

    fee_collected_percentage = (total_collected_fee / total_fee_estimate) * 100
    fee_remaining = total_fee_estimate - total_collected_fee
    percent_remaining = (fee_remaining / total_fee_estimate) * 100

    # Layout
    st.subheader("Fee Charge", divider="gray")
    fee_col1, fee_col2, fee_col3 = st.columns(3)

    # Display Metrics
    fee_col1.markdown(f"""
    <div class="total-subscribers-box">
        <p>Total Fee Estimate (LAK)</p>
        <h2>{total_fee_estimate:,}</h2>
        <h6>(100%)</h6>
    </div>
    """, unsafe_allow_html=True)

    fee_col2.markdown(f"""
    <div class="total-subscribers-box">
        <p>Total Fee Collected (LAK)</p>
        <h2>{total_collected_fee:,}</h2>
        <h6>({fee_collected_percentage:.2f}%)</h6>
    </div>
    """, unsafe_allow_html=True)

    fee_col3.markdown(f"""
    <div class="total-subscribers-box">
        <p>Total Fee Remaining (LAK)</p>
        <h2>{fee_remaining:,}</h2>
        <h6>({percent_remaining:.2f}%)</h6>
    </div>
    """, unsafe_allow_html=True)

    # fee_col1.markdown(
    # """
    # <div class="total-subscribers-box">
    #     <p>Total Fee Estimate (LAK)</p>
    #     <h2>{:,}</h2>
    # </div>
    # """.format(data['total_fee_estimate'].sum()),
    # unsafe_allow_html=True,
    # )

    # fee_col2.markdown(
    # """
    # <div class="total-subscribers-box">
    #     <p>Total Fee Collected (LAK)</p>
    #     <h2>{:,}</h2>
    # </div>
    # """.format(data['total_collected_fee'].sum()),
    # unsafe_allow_html=True,
    # )
   


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
    service_col1.metric("Total Fee Estimate MBB (LAK)", f"{data['total_fee_charge_mbb'].sum():,}")
    service_col2.metric("Total Fee Collected MBB (LAK)", f"{data['total_collected_fee_mbb'].sum():,}")
    service_col3.metric("Total Fee Estimate FBB (LAK)", f"{data['total_fee_charge_fbb'].sum():,}")
    service_col4.metric("Total Fee Collected FBB (LAK)", f"{data['total_collected_fee_fbb'].sum():,}")

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
