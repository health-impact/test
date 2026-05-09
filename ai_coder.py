import google.generativeai as genai
import os
import re

# 1. إعداد الاتصال بـ Gemini
# تأكد أنك أضفت GEMINI_API_KEY في إعدادات Secrets في GitHub
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

# 2. قراءة ملف الموقع الحالي (index.html)
with open("index.html", "r", encoding="utf-8") as f:
    current_code = f.read()

# 3. صياغة الطلب لجيمني
# يمكنك تعديل النص بين القوسين أدناه لتغيير ما يفعله الذكاء الاصطناعي تلقائياً
prompt = f"""
أنت مبرمج خبير. هذا هو كود HTML الحالي لموقعي:
{current_code}

المطلوب منك:
1. إضافة زر لمشاركة النصيحة الطبية على فيسبوك.
2. إضافة زر لنسخ النصيحة الحالية.
3. التأكد من أن التنسيق (CSS) يظل متناسقاً مع ألوان الموقع.
4. أعد لي كود HTML الكامل للموقع بعد التعديل.
ملاحظة: لا تشرح لي ماذا فعلت، فقط أعطني الكود الكامل مباشرة.
"""

# 4. طلب الكود الجديد من جيمني
response = model.generate_content(prompt)
new_code = response.text

# 5. تنظيف الكود من علامات Markdown (مثل ```html) إذا وجدت
clean_code = re.sub(r'```html\n|```', '', new_code)

# 6. حفظ الكود الجديد في الملف
with open("index.html", "w", encoding="utf-8") as f:
    f.write(clean_code.strip())

print("تم تحديث الموقع بنجاح بواسطة الكلاود!")
