import streamlit as st
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ตั้งค่าหน้าหลักของแอป
st.set_page_config(page_title="Dashboard", layout="wide")

# st.set_page_config(page_title="Dashboard", layout="wide", page_icon=":bar_chart:", initial_sidebar_state="expanded")
# st.header("Dashboard", divider="gray")
st.title("Dashboard")
# หัวข้อหลัก
st.header("Summary Total Subscribers" , divider="gray" )
host = "172.28.27.50"
dbname = "CDKPTL"
user = "smscdr"
password = "#Ltc1qaz2wsx@pg"
port = "5432"
# Fetch data immediately when connection details are filled
if host and dbname and user and password and port:
    try:
        connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cursor = connection.cursor()
        query = """
        SELECT subscriber_no, service_type, category, subscriber_status , operator_id
        FROM gov.subscribers where operator_id = 1
        """
        cursor.execute(query)
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=[desc[0] for desc in cursor.description])
        total_subscribers = len(df)
        total_mbb = df[df["category"] == "MBB"].shape[0]
        total_fbb = df[df["category"] == "FBB"].shape[0]
        total_operator_ltc = df[df["operator_id"] == 1].shape[0]
        subscriber_status_active = df[df["subscriber_status"] == "active"].shape[0]
        total_operator_tplus = df[df["operator_id"] == 3].shape[0]
        total_operator_etl = df[df["operator_id"] == 2].shape[0]
        total_operator_unitel = df[df["operator_id"] == 4].shape[0]       
        total_operator_best = df[df["operator_id"] == 5].shape[0]

        # Query for Subscriber M-Phone metric
        mphone_query = """
        SELECT SUM(amount) 
        FROM gov.fee_charge_logs 
        WHERE operator_id = 1 AND subscriber_no LIKE '85620%'
        """
        cursor.execute(mphone_query)
        subscriber_mphone = cursor.fetchone()[0] or 0

        subscriber_summary = (
            df.groupby(["service_type", "category", "subscriber_status", "operator_id"])
            .size()
            .reset_index(name="Count")
        )
        # # คอลัมน์สำหรับแสดงข้อมูลสรุป
        

        def custom_metric(title, value, size="30px", color="#4CAF50", border_color="#ddd", bg_color="#f9f9f9"):
            st.markdown(
                f"""
                <div style="
                text-align: center; 
                padding: 15px;
                border: 2px solid {border_color}; 
                border-radius: 10px; 
                background-color: {bg_color};
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            ">
                <span style="font-size: 14px; font-weight: bold; color: gray;">{title}</span><br>
                <span style="font-size: {size}; font-weight: bold; color: {color};">{value}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ข้อมูลสรุปพร้อมจุดคั่นและขนาดใหญ่

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            custom_metric("Total Subscribers", f"{total_subscribers:,}", size="40px", color="black", border_color="#f0f3f4", bg_color="#f0f3f4")
        with col2:
            custom_metric("Subscriber Active", f"{subscriber_status_active:,}", size="40px", color="black", border_color="#f0f3f4", bg_color="#f0f3f4")
        with col3:
            custom_metric("Fee Total M-Phone", f"{subscriber_mphone:,.2f}", size="40px", color="black", border_color="#f0f3f4", bg_color="#f0f3f4")
        with col4:
            custom_metric("Subscriber Win-Phone", f"{total_operator_tplus:,}", size="40px", color="black", border_color="#f0f3f4", bg_color="#f0f3f4")
        



#########################################################################################
        # st.header("Subscriber Status" , divider="gray" )
        # # สร้าง Doughnut Charts สำหรับ operator_id แต่ละตัว
        # fig, axes = plt.subplots(1, 5, figsize=(20, 6), sharey=True)  # 5 กราฟใน 1 แถว

        # # ตั้งค่าชื่อ Operator
        # operator_labels = {
        #     1: "LTC",
        #     2: "ETL",
        #     3: "TPLUS",
        #     4: "UNITEL",
        #     5: "BEST"
        # }

        # # วนลูปสร้างกราฟ Doughnut Chart สำหรับแต่ละ operator_id
        # for i, operator_id in enumerate(range(1, 6)):  # operator_id = 1 ถึง 5
        #     operator_data = df[df["operator_id"] == operator_id]["subscriber_status"].value_counts()
        #     wedges, texts, autotexts = axes[i].pie(
        #         operator_data,
        #         labels=operator_data.index,
        #         autopct='%1.1f%%',
        #         startangle=90,
        #         colors=['#6495ED', '#CD5C5C'],  # สีของ Doughnut Chart
        #         wedgeprops={'edgecolor': 'white'} # เพิ่มขอบสีขาว
        #     )
        #     # เพิ่มวงกลมตรงกลาง (ทำให้เป็นโดนัท)
        #     center_circle = plt.Circle((0, 0), 0.35, fc='white')  # 40% ของกราฟถูกเจาะเป็นวงกลม
        #     axes[i].add_artist(center_circle)

        #     # ตั้งค่าชื่อกราฟ
        #     axes[i].set_title(f"{operator_labels[operator_id]} Subscribers", fontsize=12)

        # # ตั้งค่าพื้นหลังของกราฟแต่ละอัน
        # axes[i].set_facecolor('#f0f3f4')  # เปลี่ยนพื้นหลังเป็นสีเทาอ่อน

        # # ปรับแต่ง Layout
        # plt.tight_layout()

        # # แสดงกราฟใน Streamlit
        # st.pyplot(fig)



#########################################################################################

    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

