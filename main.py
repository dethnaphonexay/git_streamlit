import streamlit as st

# Set up page configuration
st.set_page_config(page_title="Dashboard", layout="wide")

# Define available pages
pages = {
    "Home": "home.py",
    "LTC": "ltc.py",
    "ETL": "etl.py",
    "UNITEL": "unitel.py",
    "TPLUS": "tplus.py",
    "BEST": "best.py",
}

# Sidebar navigation
st.sidebar.title("FEES CHARGE")
page_selection = st.sidebar.radio("Select a Page", list(pages.keys()))

# Simulate page execution (in practice, you need to modularize the code for each page)
if page_selection == "Home":
    st.title("Home Page")
    st.write("Welcome to the Dashboard!")
elif page_selection == "LTC":
    st.title("LTC Dashboard")
    st.write("Data for LTC...")
elif page_selection == "ETL":
    st.title("ETL Dashboard")
    st.write("Data for ETL...")
elif page_selection == "UNITEL":
    st.title("UNITEL Dashboard")
    st.write("Data for UNITEL...")
elif page_selection == "TPLUS":
    st.title("TPLUS Dashboard")
    st.write("Data for TPLUS...")
elif page_selection == "BEST":
    st.title("BEST Dashboard")
    st.write("Data for BEST...")
