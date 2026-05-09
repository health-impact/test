import google.generativeai as genai
import os
import re

# 1. إعداد الاتصال
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# 2. البحث عن الموديل المتاح تلقائياً لتجنب خطأ 404
model_name = 'gemini-1.5-flash' # الافتراضي
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            model_name = m.name
            break
except:
    model_name = 'models/gemini-1.5-flash'

model = genai.GenerativeModel(model_name)

# 3. قراءة الملف
with open("index.html", "r", encoding="utf-8") as f:
    current_code = f.read()

# 4. الطلب
prompt = f"قم بإضافة أزرار مشاركة فيسبوك ونسخ النصيحة لكود HTML التالي مع الحفاظ على التنسيق: {current_code}"

# 5. التنفيذ
try:
    response = model.generate_content(prompt)
    new_code = response.text
    # تنظيف الكود
    clean_code = re.sub(r'```html\n|```', '', new_code)
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(clean_code.strip())
    print(f"Success using model: {model_name}")
except Exception as e:
    print(f"Error: {e}")
