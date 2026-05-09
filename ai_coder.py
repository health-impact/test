import google.generativeai as genai
import os
import re

# 1. إعداد الاتصال بجيمني
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# 2. اختيار الموديل المتاح تلقائياً
model_name = 'gemini-1.5-flash'
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            model_name = m.name
            break
except:
    model_name = 'models/gemini-1.5-flash'

model = genai.GenerativeModel(model_name)

# 3. قراءة ملف الموقع الحالي
with open("index.html", "r", encoding="utf-8") as f:
    current_code = f.read()

# 4. صياغة الطلب (البرومبت) بشكل صارم لمنع النصوص الزائدة
prompt = f"""
خذهذا الكود: {current_code}

المطلوب:
1. أضف أزرار مشاركة فيسبوك وواتساب وزر نسخ النصيحة لكل بطاقة نصيحة.
2. اجعل التصميم متناسقاً تماماً مع ألوان الموقع الحالية.
3. أعد لي كود HTML الكامل فقط.
4. اضافة صورة للرئيسية للموقع لها علاقة بالمحتوى.
5. اجعل مكتبة للابحاث في مجال الصحة العامة.

مهم جداً وقواعد صارمة:
- ممنوع كتابة أي كلمة خارج كود الـ HTML.
- ابدأ مباشرة بـ <!DOCTYPE html>.
- لا تكتب "إليك الكود" أو "بالتأكيد" أو أي شرح.
- لا تستخدم علامات الماركدوان مثل ```html.
"""

# 5. طلب الكود وتنظيفه
try:
    response = model.generate_content(prompt)
    raw_text = response.text
    
    # محاولة استخراج الكود فقط بين وسوم html لضمان النظافة
    match = re.search(r'<!DOCTYPE html>.*</html>', raw_text, re.DOTALL | re.IGNORECASE)
    if match:
        clean_code = match.group(0)
    else:
        # إذا لم يجد الوسوم، يقوم بإزالة علامات الماركدوان التقليدية
        clean_code = re.sub(r'```html\n|```', '', raw_text)

    # 6. حفظ الكود النظيف في الملف
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(clean_code.strip())
    print(f"تم التحديث بنجاح باستخدام موديل: {model_name}")

except Exception as e:
    print(f"حدث خطأ أثناء التحديث: {e}")
