import streamlit as st
from streamlit_gsheets import GSheetsConnection

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Check Your Role", page_icon="🕵️")

st.title("🎮 กิจกรรมค้นหาบทบาท")
st.write("กรุณาใส่เลขนักศึกษาเพื่อตรวจสอบกลุ่มและหน้าที่ของคุณ")

# เชื่อมต่อ Google Sheets (ค่า URL จะไปตั้งใน Secrets ทีหลัง)
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(spreadsheet="https://docs.google.com/spreadsheets/d/1-qGlWR5Fa9TfaCO4Nae8IVATESt3fKbuO6vWp9tcSGA/edit?usp=sharing")

# ช่องรับข้อมูล
student_id_input = st.text_input("เลขนักศึกษา", placeholder="เช่น 6XXXXXXX")

if st.button("ตรวจสอบข้อมูล"):
    if student_id_input:
        # ค้นหาใน Column 'student_id' (ต้องตรงกับหัวตารางใน Google Sheet)
        result = df[df['student_id'].astype(str) == student_id_input]
        
        if not result.empty:
            group = result.iloc[0]['group']
            
            st.divider()
            st.subheader(f"กลุ่มของคุณคือ: {group}")
            
            # ถ้าเป็น Imposter ให้โชว์สีแดงเตือน
            if group.lower() == "imposter":
                st.error(f"บทบาทของคุณคือ: {group} 🚨")
            else:
                st.success(f"บทบาทของคุณคือ: {group} ✅")
        else:
            st.warning("❌ ไม่พบเลขนักศึกษานี้ในระบบ กรุณาลองใหม่อีกครั้ง")
    else:
        st.info("กรุณากรอกเลขนักศึกษาก่อนกดปุ่ม")