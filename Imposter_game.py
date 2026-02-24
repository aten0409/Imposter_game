import streamlit as st
from streamlit_gsheets import GSheetsConnection

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Find Your group",layout="centered", page_icon="🕵️")

# เชื่อมต่อ Google Sheets (ค่า URL จะไปตั้งใน Secrets ทีหลัง)
conn = st.connection("gsheets", type=GSheetsConnection)
url = "https://docs.google.com/spreadsheets/d/1-qGlWR5Fa9TfaCO4Nae8IVATESt3fKbuO6vWp9tcSGA/edit?usp=sharing"
df = conn.read(spreadsheet=url, ttl=30)

# 3. ใช้ Session State เพื่อคุมการสลับหน้าจอ
if 'screen' not in st.session_state:
    st.session_state.screen = 'input' # หน้าเริ่มต้นคือหน้า input
    st.session_state.user_data = None

# --- ส่วนของการแสดงผล ---

# 4. หน้ากรอกข้อมูล (โชว์เฉพาะเมื่อ screen == 'input')
if st.session_state.screen == 'input':
    st.title("FIND YOUR ROLE!!!")
    st.write("กรุณาใส่เลขนักศึกษาเพื่อตรวจสอบบทบาทของคุณ")
    
    student_id = st.text_input("รหัสนักศึกษา", placeholder="6XXXXXXX")
    
    if st.button("ตรวจสอบข้อมูล"):
        if student_id:
            result = df[df['student_id'].astype(str) == student_id]
            
            if not result.empty:
                st.session_state.user_data = result.iloc[0]
                st.session_state.screen = 'result' # สั่งเปลี่ยนหน้า
                st.rerun()
            else:
                st.error("❌ ไม่พบเลขนักศึกษานี้ในระบบ")
        else:
            st.warning("กรุณากรอกเลขนักศึกษาก่อนครับ")

# 5. หน้าแสดงผลเต็มจอ (โชว์เฉพาะเมื่อ screen == 'result')
elif st.session_state.screen == 'result':
    data = st.session_state.user_data
    group = data['group']
    
    # เช็กว่าเป็น Imposter หรือไม่ (เช็กจากคำใน Column group)
    is_imposter = "imposter" in str(group).lower()
    bg_color = "#FF4B4B" if is_imposter else "#00C853" # แดงถ้าใช่, เขียวถ้าไม่ใช่
    
    # ใช้ CSS ปรับพื้นหลังทั้งหน้าและทำให้ตัวหนังสือใหญ่
    st.markdown(f"""
        <style>
            /* ปรับพื้นหลังของแอปทั้งหมด */
            .stApp {{
                background-color: {bg_color};
            }}
            /* ซ่อนเมนูและปุ่มด้านบนเพื่อให้ดูเป็นแอปเต็มจอ */
            header {{visibility: hidden;}}
            footer {{visibility: hidden;}}
            
            .main-container {{
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 75vh;
                color: white;
                text-align: center;
                padding: 10px;
            }}

            /* ขนาดสำหรับหน้าจอคอมพิวเตอร์ */
            .label-text {{
                font-size: 30px;
                margin-bottom: 20px;
            }}
            .huge-text {{
                font-size: 80px !important;
                font-weight: bold;
                line-height: 1.1;
                word-wrap: break-word;
                max-width: 90vw;
            }}

            /* ปรับขนาดสำหรับโทรศัพท์มือถือ (หน้าจอเล็กกว่า 600px) */
            @media only screen and (max-width: 600px) {{
                .label-text {{
                    font-size: 6vw; /* ปรับตามความกว้างหน้าจอ */
                    margin-bottom: 10px;
                }}
                .huge-text {{
                    font-size: 14vw !important; /* ปรับให้พอดีจอโทรศัพท์ */
                }}
                .main-container {{
                    height: 60vh;
                }}
            }}
        </style>
        
        <div class="main-container">
            <div class="label-text">บทบาทของคุณคือ</div>
            <div class="huge-text">{group}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # ปุ่มย้อนกลับแบบ Minimal
    if st.button("BACK"):
        st.session_state.screen = 'input'
        st.rerun()