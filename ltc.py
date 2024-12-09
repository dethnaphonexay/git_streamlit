import streamlit as st
import pandas as pd
import plotly.express as px

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
    .total-subscribers-box {
        background-color: #ffffff;
        padding: 20px;
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

# กรองข้อมูลเฉพาะของ LTC
ltc_data = data[data['operator_name'] == 'LTC']

# ตรวจสอบว่ามีข้อมูลหรือไม่
if not ltc_data.empty:
    st.title("Dashboard Monitor Fee Charge LTC")

    # แสดง Total Subscribers แบบ metric
    total_subscribers = ltc_data['total_sub'].sum()
    st.markdown(
        f"""
        <div class="total-subscribers-box">
            Total Subscribers (LTC): {total_subscribers:,}
        </div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(6)
    cols[0].markdown(
        """
        <div class="metric-card">
            <p>Total Subscribers</p>
            <h2>{:,}</h2>
        </div>
        """.format(ltc_data['total_sub'].sum()),
        unsafe_allow_html=True,
    )
    cols[1].markdown(
        """
        <div class="metric-card">
            <p>MBB</p>
            <h2>{:,}</h2>
        </div>
        """.format(ltc_data['mbb'].sum()),
        unsafe_allow_html=True,
    )
    cols[2].markdown(
        """
        <div class="metric-card">
            <p>FBB</p>
            <h2>{:,}</h2>
        </div>
        """.format(ltc_data['fbb'].sum()),
        unsafe_allow_html=True,
    )
    cols[3].markdown(
        """
        <div class="metric-card">
            <p>Active MBB</p>
            <h2>{:,}</h2>
        </div>
        """.format(ltc_data['active_mbb'].sum()),
        unsafe_allow_html=True,
    )
    cols[4].markdown(
        """
        <div class="metric-card">
            <p>Active FBB</p>
            <h2>{:,}</h2>
        </div>
        """.format(ltc_data['active_fbb'].sum()),
        unsafe_allow_html=True,
    )
    cols[5].markdown(
        """
        <div class="metric-card">
            <p>Disable MBB</p>
            <h2>{:,}</h2>
        </div>
        """.format(ltc_data['disable_mbb'].sum()),
        unsafe_allow_html=True,
    )

    # Fee Charge Summary
    st.subheader("Fee Charge (LTC)", divider="gray")
    fee_col1, fee_col2 = st.columns(2)
    # fee_col1.metric("Total Fee Estimate", f"{ltc_data['total_fee_estimate'].sum():,}")
    # fee_col2.metric("Total Fee Collected", f"{ltc_data['total_collected_fee'].sum():,}")
    with fee_col1:
    # สร้างกรอบ
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("<h5>Total Fee Estimate</h5>", unsafe_allow_html=True)
        st.metric("", f"{ltc_data['total_fee_estimate'].sum():,}")
        st.markdown('</div>', unsafe_allow_html=True)

    with fee_col2:
    # สร้างกรอบ
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("<h5>Total Fee Collected</h5>", unsafe_allow_html=True)
        st.metric("", f"{ltc_data['total_collected_fee'].sum():,}")
        st.markdown('</div>', unsafe_allow_html=True)

    # รายละเอียดค่าธรรมเนียม MBB และ FBB
    st.subheader("Details by Service Type (LTC)", divider="gray")
    service_col1, service_col2, service_col3, service_col4 = st.columns(4)
    service_col1.metric("Total Fee Estimate MBB", f"{ltc_data['total_fee_charge_mbb'].sum():,}")
    service_col2.metric("Total Fee Collected MBB", f"{ltc_data['total_collected_fee_mbb'].sum():,}")
    service_col3.metric("Total Fee Estimate FBB", f"{ltc_data['total_fee_charge_fbb'].sum():,}")
    service_col4.metric("Total Fee Collected FBB", f"{ltc_data['total_collected_fee_fbb'].sum():,}")

    # Pie Charts
    st.subheader("Visualizations (LTC)", divider="gray")
    pie_col1, pie_col2, pie_col3 = st.columns(3)

    # Total fee collected vs estimated
    fig1 = px.pie(
        values=[
            ltc_data['total_collected_fee'].sum(),
            ltc_data['total_fee_estimate'].sum() - ltc_data['total_collected_fee'].sum()
        ],
        names=["Collected", "Remaining"],
        title="Total Fee Collected (LTC)"
    )
    pie_col1.plotly_chart(fig1)

    # Fee MBB collected vs estimated
    fig2 = px.pie(
        values=[
            ltc_data['total_collected_fee_mbb'].sum(),
            ltc_data['total_fee_charge_mbb'].sum() - ltc_data['total_collected_fee_mbb'].sum()
        ],
        names=["Collected MBB", "Remaining MBB"],
        title="MBB Fee Collected (LTC)"
    )
    pie_col2.plotly_chart(fig2)

    # Fee FBB collected vs estimated
    fig3 = px.pie(
        values=[
            ltc_data['total_collected_fee_fbb'].sum(),
            ltc_data['total_fee_charge_fbb'].sum() - ltc_data['total_collected_fee_fbb'].sum()
        ],
        names=["Collected FBB", "Remaining FBB"],
        title="FBB Fee Collected (LTC)"
    )
    pie_col3.plotly_chart(fig3)
else:
    st.warning("No data available for LTC.")
