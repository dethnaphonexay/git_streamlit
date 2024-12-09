import streamlit as st

# ตั้งค่าหน้าก่อนทำอย่างอื่น
st.set_page_config(page_title="Dashboard", layout="wide")

pages = {
    "MENU": [
        st.Page("home.py", title="Home"),
    ],
    "OPERATOR": [
        st.Page("ltc.py", title="LTC"),
        st.Page("etl.py", title="ETL"),
        st.Page("unitel.py", title="UNITEL"),
        st.Page("tplus.py", title="TPLUS"),
        st.Page("best.py", title="BEST"),
    ],
}
st.sidebar.title("FEES CHARGE")
pg = st.navigation(pages)
pg.run()

