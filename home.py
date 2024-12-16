import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_echarts import st_echarts
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
file_path = r"operator_data.csv"

# โหลดข้อมูล
data = load_data_from_path(file_path)
data["image_path"] = ["p_ltc.jpg", "p_tplus.jpg", "p_unitel.jpg", "p_etl.jpg", "p_best.jpg"]

# ตรวจสอบว่ามีข้อมูลหรือไม่
if not data.empty:
    # ส่วนของ Dashboard
    st.title("Dashboard Monitor Fee Charge")

    # Total Subscribers
    st.subheader("Operator Total Subscribers", divider="gray")
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

                st.image(row.image_path, width=100 ,)  # Add image
                
                st.markdown(
                    f"""
                    <div class="metric-box">
                        <h6>{row.operator_name}</h6>
                        <p><b></b> <span style="font-size: 30px; font-weight: bold;">{row.total_sub:,}</span></p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # Fee Charge Summary
    st.subheader("Fee Charge", divider="gray")
    total_fee_estimate = data['total_fee_estimate'].sum()
    total_collected_fee = data['total_collected_fee'].sum()

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
    st.subheader("Details by Service Type (LTC)", divider="gray")
    service_col1, service_col2, service_col3, service_col4 = st.columns(4)
    service_col1.metric("Total Fee Estimate MBB (LAK)", f"{data['total_fee_charge_mbb'].sum():,}")
    service_col2.metric("Total Fee Collected MBB (LAK)", f"{data['total_collected_fee_mbb'].sum():,}")
    service_col3.metric("Total Fee Estimate FBB (LAK)", f"{data['total_fee_charge_fbb'].sum():,}")
    service_col4.metric("Total Fee Collected FBB (LAK)", f"{data['total_collected_fee_fbb'].sum():,}")

    # Pie Charts
    st.subheader("Visualizations", divider="gray")
    pie_col1, pie_col2, pie_col3 = st.columns(3)
    fig1 = px.pie(
        values=[
            data['total_collected_fee'].sum(),
            data['total_fee_estimate'].sum() - data['total_collected_fee'].sum()
        ],
        names=["Collected", "Remaining"],
        title="Total Fee Collected"
    )
    pie_col1.plotly_chart(fig1)

    fig2 = px.pie(
        values=[
            data['total_collected_fee_mbb'].sum(),
            data['total_fee_charge_mbb'].sum() - data['total_collected_fee_mbb'].sum()
        ],
        names=["Collected MBB", "Remaining MBB"],
        title="MBB Fee Collected"
    )
    pie_col2.plotly_chart(fig2)

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

st.subheader("Daily Analysis Dashboard", divider="gray")
options = {
    "title": {"text": "Subscribers Daily"},
    "tooltip": {"trigger": "axis"},
    "legend": {"data": ["LTC", "ETL", "UNITEL", "TPLUS", "BEST"]},
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
           
             "data": [99796, 95090, 130030, 38936, 133799, 14040, 106034, 125765, 60335, 123086, 82329, 112472, 148613, 133634, 117956, 76377, 48966, 56890, 15605, 8432, 98921, 77448, 61190, 61840, 30937, 143744],
        },
        {
            "name": "ETL",
            "type": "line",
            
            "data": [37888, 41535, 25513, 31117, 27273, 81302, 56879, 44847, 3108, 841, 49498, 8586, 70179, 74521, 74849, 3016, 35021, 35627, 50724, 29234, 67530, 21237, 78136, 27179, 4559, 45257],
        },
        {
            "name": "UNITEL",
            "type": "line",
           
            "data": [244766, 115029, 95817, 255190, 133356, 160984, 100495, 220173, 242412, 84693, 104486, 219746, 52761, 20907, 74036, 96754, 71091, 134701, 5193, 86389, 52694, 234828, 82094, 123973, 198152, 35134],
        },
        {
            "name": "TPLUS",
            "type": "line",
            
            "data": [58388, 56334, 47516, 2166, 19603, 7409, 13217, 50833, 33224, 41158, 67006, 4515, 36549, 18585, 32284, 33349, 38106, 10570, 54751, 70499, 67129, 56685, 24272, 39996, 39392, 61705],
        },
        {
            "name": "BEST",
            "type": "line",
            
            "data": [37, 98, 231, 245, 92, 135, 290, 103, 35, 214, 30, 273, 181, 80, 80, 262, 70, 247, 200, 321, 221, 40, 29, 23, 321, 100],
        },
    ],
}


st_echarts(options=options, height="400px")
options = {
    "title": {"text": "Fee Collected Daily (LAK)"},
    "tooltip": {"trigger": "axis"},
    "legend": {"data": ["LTC", "ETL", "UNITEL", "TPLUS", "BEST"]},
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
             "data": [ 258468000,254823000,231264000,230097000,227145000,224217000,297653000,303328000,350411000,231054000,239391000,269466000,230094000,248592000,198227000,226527000,215487000,204258000,345895000,289291000,238869000,339407000,205179000,264246000,244377000,399959000],
        },
        {
            "name": "ETL",
            "type": "line",
            "data": [ 173017000,85575000,133917000,112050000,84075000,120594000,126978000,97062000,122556000,147021000,99261000,129645000,89061000,125868000,92460000,79920000,113514000,145515000,118551000,83916000,123130000,97920000,141405000,97753000,105807000,81963000],
        },
        {
            "name": "UNITEL",
            "type": "line", 
            "data": [ 413358000,406551000,401016000,228723000,433968000,340346000,320610000,338646000,284000000,259800000,318306000,374469000,425094000,426669000,335640000,381273000,432828000,388365000,322686000,383400000,420942000,378636000,457831000,423784000,357022000,459239000],
        },
        {
            "name": "TPLUS",
            "type": "line",
            "data": [ 140208000,77716000,102669000,123494000,116295000,136908000,91455000,123639000,71966000,83916000,78293000,134120000,156171000,126934000,90234000,117093000,127134000,82918000,133482000,121887000,81396000,138597000,65570000,90127000,72695000,48146000],
        },
        {
            "name": "BEST",
            "type": "line",        
            "data": [ 321000,615000,552000,648000,696000,600000,501000,735000,342000,480000,750000,696000,312000,414000,618000,495000,729000,468000,465000,582000,423000,694000,444000,300000,455000,241000],
        },
    ],
}
st_echarts(options=options, height="400px")