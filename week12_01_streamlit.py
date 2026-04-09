import streamlit as st
st.set_page_config(page_title="Example", layout="wide")
st.title("This is an example page")

# Two columns
col1, col2 = st.columns([2,1])
with col1:
    st.write("Main Content")
with col2:
    st.write("Side Panel")

with st.sidebar:
    model = st.selectbox("Model", ["gpt-4o-mini", "gpt-oss:20b"])