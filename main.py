import streamlit as st

# ตั้งค่าหน้าก่อนทำอย่างอื่น
st.set_page_config(page_title="Dashboard", layout="wide")

# เพิ่มโลโก้
# try:
#     add_logo("C:/Users/Asus/Desktop/Project_stremlit/images/150.png", height=200)
# except Exception as e:
#     st.error(f"ไม่สามารถเพิ่มโลโก้ได้: {e}")

pages = {
    "FEES CHANGE":[],
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

pg = st.navigation(pages)
pg.run()