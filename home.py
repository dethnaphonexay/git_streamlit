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
file_path = "operator_data.csv"  # แก้ไข path ตรงนี้เป็น path จริงของไฟล์ CSV บนระบบของคุณ
# file_path = r"C:\Users\Asus\Desktop\Project_stremlit\git_streamlit\data\operator_data.csv"
# funded.to_csv(os.path.join(path, 'operator_data.csv')
file_path = r"git_streamlit\data\operator_data.csv"
# โหลดข้อมูล
<<<<<<< HEAD
st.title("Dashboard Monitor Fee Charge")

# Define the data
datas = {
    "operator_name": ["LTC", "ETL", "TPLUS", "UNITEL", "BEST"],
    "total_sub": [2100356, 1087876, 1210692, 2325848, 807054],
    "active_sub": [1850000, 985420, 1005486, 1956896, 752365],
    "disable_sub": [250356, 102456, 205206, 368952, 54689],
    "mbb": [1943527, 1027682, 1210692, 2118235, 795863],
    "fbb": [156829, 60194, 0, 207613, 11191],
    "active_mbb": [1713725, 940278, 1005486, 1765155, 743217],
    "disable_mbb": [229802, 87404, 205206, 353080, 52646],
    "active_fbb": [136275, 45142, 0, 191741, 9148],
    "disable_fbb": [20554, 15052, 0, 15872, 2043],
    "total_fee_charge_mbb": [5141175000, 2820834000, 3016458000, 5295465000, 2229651000],
    "total_fee_charge_fbb": [681375000, 225710000, 0, 958705000, 45740000],
    "total_fee_estimate": [5822550000, 3046544000, 3016458000, 6254170000, 2275391000],
    "total_collected_fee_mbb": [3907293000, 2256667200, 2714812200, 4501145250, 2162761470],
    "total_collected_fee_fbb": [647306250, 196367700, 0, 853247450, 43453000],
    "total_collected_fee": [4554599250, 2453034900, 2714812200, 5354392700, 2206214470],
}

# Create the DataFrame
data = pd.DataFrame(datas)


=======
data = load_data_from_path(file_path)
>>>>>>> 61d415c767d15a49ab4ca41014855362e8df5c98

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

options = {
    "title": {"text": "Subscribers"},
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