import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_echarts import st_echarts
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
        text-align: center;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .total-subscribers-box {
        background-color:rgb(239, 241, 241);
        padding: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        margin: 20px 0;
    }
    .center { 
        text-align: center;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ฟังก์ชันสำหรับดึงข้อมูลจาก CSV
@st.cache_data
def load_data_from_path(file_path):
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        st.error(f"Error reading the file: {e}")
        return pd.DataFrame()

# ระบุ path ของไฟล์ CSV
# file_path = "data.csv"  # แก้ไข path ตรงนี้เป็น path จริงของไฟล์ CSV บนระบบของคุณ
# file_path = r"C:\Users\Asus\Desktop\Project_stremlit\git_streamlit\data\operator_data.csv"
file_path = r"operator_data.csv"
# โหลดข้อมูล
data = load_data_from_path(file_path)

# กรองข้อมูลเฉพาะของ LTC
unitel_data = data[data['operator_name'] == 'UNITEL']

# ตรวจสอบว่ามีข้อมูลหรือไม่
if not data.empty:
    # สร้างกรอบรวมผู้ให้บริการทั้งหมด
    if not unitel_data.empty:
        st.title("Dashboard Monitor Fee Charge UNITEL")
    st.subheader("Total Subscribers", divider="gray")
    total_subscribers = unitel_data['total_sub'].sum()
    st.markdown(
        f"""
        <div class="total-subscribers-box">
            Total Subscribers: {total_subscribers:,}
        </div>
        """,
        unsafe_allow_html=True,
    )
    cols = st.columns(6)
    cols[0].markdown(
        """
        <div class="center">
            <p>MBB</p>
            <h2>{:,}</h2>
        </div>
        """.format(unitel_data['mbb'].sum()),
        unsafe_allow_html=True,
    )
    cols[1].markdown(
        """
        <div class="center">
            <p>FBB</p>
            <h2>{:,}</h2>
        </div>
        """.format(unitel_data['fbb'].sum()),
        unsafe_allow_html=True,
    )
    cols[2].markdown(
        """
        <div class="center">
            <p>Active MBB</p>
            <h2>{:,}</h2>
        </div>
        """.format(unitel_data['active_mbb'].sum()),
        unsafe_allow_html=True,
    )
    cols[3].markdown(
        """
        <div class="center">
            <p>Active FBB</p>
            <h2>{:,}</h2>
        </div>
        """.format(unitel_data['active_fbb'].sum()),
        unsafe_allow_html=True,
    )
    cols[4].markdown(
        """
        <div class="center">
            <p>Disable MBB</p>
            <h2>{:,}</h2>
        </div>
        """.format(unitel_data['disable_mbb'].sum()),
        unsafe_allow_html=True,
    )
    cols[5].markdown(
        """
        <div class="center">
            <p>Disable FBB</p>
            <h2>{:,}</h2>
        </div>
        """.format(unitel_data['disable_fbb'].sum()),
        unsafe_allow_html=True,
    )

    # Fee Charge Summary
    st.subheader("Fee Charge", divider="gray")
    total_fee_estimate = unitel_data['total_fee_estimate'].sum()
    total_collected_fee = unitel_data['total_collected_fee'].sum()

    fee_collected_percentage = (total_collected_fee / total_fee_estimate) * 100
    fee_remaining = total_fee_estimate - total_collected_fee
    percent_remaining = (fee_remaining / total_fee_estimate) * 100

    fee_col1, fee_col2, fee_col3 = st.columns(3)
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

     # รายละเอียดค่าธรรมเนียม MBB และ FBB
    st.subheader("Details by Service Type (UNITEL)", divider="gray")
    service_col1, service_col2, service_col3, service_col4 = st.columns(4)
    service_col1.metric("Total Fee Estimate MBB (LAK)", f"{unitel_data['total_fee_charge_mbb'].sum():,}")
    service_col2.metric("Total Fee Collected MBB (LAK)", f"{unitel_data['total_collected_fee_mbb'].sum():,}")
    service_col3.metric("Total Fee Estimate FBB (LAK)", f"{unitel_data['total_fee_charge_fbb'].sum():,}")
    service_col4.metric("Total Fee Collected FBB (LAK)", f"{unitel_data['total_collected_fee_fbb'].sum():,}")

    # Pie Charts
    st.subheader("Visualizations", divider="gray")
    pie_col1, pie_col2, pie_col3 = st.columns(3)
    fig1 = px.pie(
        values=[
            unitel_data['total_collected_fee'].sum(),
            unitel_data['total_fee_estimate'].sum() - unitel_data['total_collected_fee'].sum()
        ],
        names=["Collected", "Remaining"],
        title="Total Fee Collected"
    )
    pie_col1.plotly_chart(fig1)

    fig2 = px.pie(
        values=[
            unitel_data['total_collected_fee_mbb'].sum(),
            unitel_data['total_fee_charge_mbb'].sum() - unitel_data['total_collected_fee_mbb'].sum()
        ],
        names=["Collected MBB", "Remaining MBB"],
        title="MBB Fee Collected"
    )
    pie_col2.plotly_chart(fig2)

    fig3 = px.pie(
        values=[
            unitel_data['total_collected_fee_fbb'].sum(),
            unitel_data['total_fee_charge_fbb'].sum() - unitel_data['total_collected_fee_fbb'].sum()
        ],
        names=["Collected FBB", "Remaining FBB"],
        title="FBB Fee Collected"
    )
    pie_col3.plotly_chart(fig3)
else:
    st.warning("No data available to display.")

st.subheader("Subscribers daily", divider="gray")
options = {
    "title": {"text": "Total"},
    "tooltip": {"trigger": "axis"},
    "axisPointer": {"type": "cross", "label": {"backgroundColor": "#6a7985"}},
    "legend": {"data": ["UNITEL"]},
    "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
    "toolbox": {"feature": {"saveAsImage": {}}},
    "xAxis": {
        "type": "category",
        "boundaryGap": False,
        "data": ["1", "2", "3", "4", "5", "6", "7", "8" , "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26"],
    },
    "yAxis": {"type": "value"},
    "series": [
        {
            "name": "LTC",
            "type": "line",
            "areaStyle": {},
            "emphasis": {"focus": "series"},         
            "data": [244766, 115029, 95817, 255190, 133356, 160984, 100495, 220173, 242412, 84693, 104486, 219746, 52761, 20907, 74036, 96754, 71091, 134701, 5193, 86389, 52694, 234828, 82094, 123973, 198152, 35134],
        },
    ],
}
st_echarts(options=options, height="400px")