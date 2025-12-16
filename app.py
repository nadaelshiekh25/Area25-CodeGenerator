import streamlit as st
import pandas as pd
import os
import csv
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="Area25 Coder", layout="centered")

# العنوان الجديد كما طلبتِ
st.title("Hello Designer!")
st.subheader("Choose your Design Type!")
st.divider()

FILE_NAME = 'product_history.csv'

# 2. القواميس (تم تحديث القائمة بالكامل)
CATEGORIES = {
    'Accent Chair': 'AC',
    'Bar Stool': 'BS',
    'Bench': 'BN',
    'Buffet': 'BF',
    'Bunk Bed': 'BB',
    'C Table': 'CT',
    'Cabinet': 'CB',
    'Center Table': 'CN',
    'Coffee Table': 'CF',
    'Console': 'CS',
    'Desk Chair': 'DKC',
    'Desk Table': 'DKT',
    'Dining Chair': 'DNC',
    'Dining Table': 'DNT',
    'King Bed': 'KB',
    'Night Stand': 'NS',
    'Ottoman': 'OT',
    'Partition': 'PR',
    'Queen Bed': 'QB',
    'Sectional Sofa': 'SS',
    'Shelf': 'SH',
    'Side Table': 'ST',
    'Single Bed': 'SB',
    'Sofa 2 seater': 'S2',
    'Sofa 3 seater': 'S3',
    'Sofa 4 seater': 'S4',
    'Stool': 'SL',
    'TV Unit': 'TV',
    'Wall Art': 'WA',
    'Wardrobe': 'WR',
    'Mirrors': 'MR',
    'Lighting': 'LG',
    'Stand': 'STD'
}

# قائمة الخامات (يمكنك زيادتها لاحقاً)
MATERIALS = {
    'Wood': 'WD',
    'Metal': 'MT',
    'Velvet': 'VL',
    'Leather': 'LT',
    'Glass': 'GL',
    'Marble': 'MB',
    'Fabric': 'FB'
}

# 3. دالة تجهيز الملف (قاعدة البيانات)
def initialize_database():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Category', 'Material', 'Generated_Code'])

# 4. دالة الحساب الذكي
def get_next_serial(prefix):
    count = 0
    if os.path.exists(FILE_NAME):
        try:
            df = pd.read_csv(FILE_NAME)
            # التأكد من أن الأعمدة نصوص لتجنب الأخطاء
            df['Generated_Code'] = df['Generated_Code'].astype(str)
            # البحث عن الأكواد التي تبدأ بنفس المقدمة
            matched = df[df['Generated_Code'].str.startswith(prefix, na=False)]
            count = len(matched)
        except:
            count = 0
    return count + 1

# --- بدء الواجهة ---
initialize_database()

# تنسيق الواجهة بشكل أنيق
col1, col2 = st.columns(2)

with col1:
    st.info("📋 **Product Details**")
    # القائمة المنسدلة للفئات
    cat_name = st.selectbox("Select Item Type", list(CATEGORIES.keys()))
    # القائمة المنسدلة للخامات
    mat_name = st.selectbox("Select Material", list(MATERIALS.keys()))

with col2:
    st.success("👀 **Preview SKU**")
    
    # تحضير الكود
    cat_code = CATEGORIES[cat_name]
    mat_code = MATERIALS[mat_name]
    prefix = f"{cat_code}-{mat_code}"
    
    # حساب الرقم القادم
    next_serial = get_next_serial(prefix)
    new_code = f"{prefix}-{next_serial:03d}"
    
    st.metric(label="New Code Generated", value=new_code)

# زر الحفظ الكبير
st.write("") # مسافة فارغة
if st.button("Generate & Save Code ", use_container_width=True):
    date_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # عملية الحفظ
    with open(FILE_NAME, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([date_now, cat_name, mat_name, new_code])
    
    st.balloons() # احتفال
    st.toast(f"Saved: {new_code}", icon="✅")
    
    # إعادة تحميل الصفحة لتحديث الجدول تلقائياً (اختياري)
    # st.rerun() 

st.divider()

# عرض السجل
st.subheader("📂 Design History")

if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
    if not df.empty:
        # ترتيب من الأحدث للأقدم
        df = df.sort_index(ascending=False)
        st.dataframe(df, use_container_width=True)
    else:
        st.caption("No designs generated yet.")
else:
    st.caption("Database created successfully.")
