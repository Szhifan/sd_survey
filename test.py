import streamlit as st

pg = st.navigation([st.Page("survey.py"), st.Page("pages/examples&instructions.py")])
pg.run()