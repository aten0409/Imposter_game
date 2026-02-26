import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Find Your Role", layout="centered", page_icon="🕵️")

@st.cache_data(ttl=300)
def get_data_dict():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        url = "https://docs.google.com/spreadsheets/d/1-qGlWR5Fa9TfaCO4Nae8IVATESt3fKbuO6vWp9tcSGA/edit?usp=sharing"
        df = conn.read(spreadsheet=url)
        return pd.Series(df['group'].values, index=df['student_id'].astype(str)).to_dict()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return {}

data_dict = get_data_dict()

if 'group_result' not in st.session_state:
    st.session_state.group_result = None

if st.session_state.group_result is None:
    st.markdown("""
        <style>
            .title-text {
                font-size: 45px;
                font-weight: bold;
                text-align: center;
                white-space: nowrap;
                margin-bottom: 20px;
                color: #FFFFFF; 
            }
            @media only screen and (max-width: 600px) {
                .title-text {
                    font-size: 8.5vw;
                }
            }
        </style>
        <div class="title-text">🔍 FIND YOUR ROLE!!!</div>
    """, unsafe_allow_html=True)
    st.write(f"กรุณาใส่รหัสนักศึกษาเพื่อตรวจสอบบทบาทของคุณ")
    
    with st.form("check_form", clear_on_submit=True):
        student_id = st.text_input("รหัสนักศึกษา", placeholder="6XXXXXXXXX")
        submit = st.form_submit_button("ตรวจสอบบทบาท", use_container_width=True)
        
        if submit:
            if student_id in data_dict:
                st.session_state.group_result = data_dict[student_id]
                st.rerun()
            else:
                st.error("❌ ไม่พบเลขนักศึกษาในระบบ")

else:
    group = st.session_state.group_result
    is_imposter = "imposter" in str(group).lower()
    bg_color = "#FF4B4B" if is_imposter else "#00C853"
    
    st.markdown(f"""
        <style>
            .stApp {{ background-color: {bg_color}; }}
            header, footer {{ visibility: hidden; }}
            
            .res-container {{
                display: flex; flex-direction: column;
                justify-content: center; align-items: center;
                height: 75vh; color: white; text-align: center;
                padding: 10px;
            }}
            .label-text {{ font-size: 30px; margin-bottom: 20px; }}
            .huge-text {{ 
                font-size: 80px !important; font-weight: bold; 
                line-height: 1.1; word-wrap: break-word; 
                max-width: 95vw; overflow-wrap: break-word;
            }}

            @media only screen and (max-width: 600px) {{
                .label-text {{ font-size: 6vw; }}
                .huge-text {{ font-size: 14vw !important; }}
                .res-container {{ height: 60vh; }}
            }}
        </style>
        <div class="res-container">
            <div class="label-text">บทบาทของคุณคือ</div>
            <div class="huge-text">{group}</div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("BACK"):
        st.session_state.group_result = None
        st.rerun()