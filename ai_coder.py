import google.generativeai as genai
import os
import re
import json
from datetime import datetime

# 1. إعداد الاتصال بجيمني واختيار الموديل المتاح تلقائياً
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model_name = 'gemini-1.5-flash'
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            model_name = m.name
            break
except: 
    model_name = 'models/gemini-1.5-flash'

model = genai.GenerativeModel(model_name)

# 2. جلب تاريخ اليوم الحالي ديناميكياً لتحديث الأخبار بناءً عليه
current_date_str = datetime.now().strftime("%Y-%m-%d")

# 3. قراءة ملف الموقع الحالي
try:
    with open("index.html", "r", encoding="utf-8") as f:
        current_code = f.read()
except FileNotFoundError:
    print("خطأ: لم يتم العثور على ملف index.html في المسار الحالي.")
    exit(1)

# 4. برومبت ذكي ومحدد: يطلب توليد بيانات مصفوفة الأخبار فقط لحماية تصميم الموقع من التخريب
prompt = f"""
أنت مبرمج محترف. المطلوب منك فقط هو توليد بيانات مصفوفة الأخبار الطبية لتاريخ اليوم وهو ({current_date_str}).
يجب أن توضع الأخبار مباشرة بعد جزئية (من نحن) في الموقع، وتركز على مجالات: مقاومة المضادات الحيوية، سلامة الأغذية، ومكافحة العدوى في المختبرات الطبية والصحة العامة.

شروط صارمة للبيانات:
1. قم بإنشاء 3 أخبار حقيقية وموثوقة ومحدثة لاهتمام القراء والشباب.
2. لا تضع حقل للتاريخ نهائياً في البيانات (أمر صارم بحذف التاريخ).
3. يجب وضع رابط صورة مباشر، عالي الجودة وشغال 100% من Unsplash يعبر بدقة دلالية عن محتوى الخبر (مثل صور أجهزة مختبرات، أطباء وفنيين، جراثيم تحت المجهر، أو أغذية سليمة) كأنها الصورة الرسمية المنشورة مع الخبر في مصدره الموثوق. ممنوع منعاً باتاً تنزيل أي خبر بدون صورة.

أريدك أن ترسل لي كود مصفوفة الجافاسكريبت فقط باسم `healthNewsData` كالتالي تماماً:
const healthNewsData = [
  {{
    id: 1,
    title: "عنوان الخبر الأول المثير والحديث",
    description: "تفاصيل الخبر الأول بدقة علمية لغير المختصين والمستند لمصادر موثوقة.",
    image: "https://images.unsplash.com/photo-..."
  }},
  ...
];

ممنوع كتابة أي مقدمات أو شروحات أو استخدام علامات الماركدوان الزائدة، ابدأ بكتابة const وانته بـ ]; فوراً.
"""

print(f"جاري طلب الأخبار الحية المحدثة لليوم {current_date_str}... ⏳")

# 5. تنفيذ الطلب وحقن المصفوفة الجديدة داخل الملف الأصلي بأمان دون المساس بالتصميم
try:
    response = model.generate_content(prompt)
    ai_news_matrix = response.text.strip()
    
    # تنظيف مخرجات الـ AI للتأكد من أنها مصفوفة صافية ومحمية
    if "```" in ai_news_matrix:
        ai_news_matrix = re.sub(r'```javascript\n|```html\n|```', '', ai_news_matrix).strip()

    # البحث عن مصفوفة الأخبار القديمة في ملفك واستبدالها بالجديدة مع الحفاظ على كل الـ CSS والـ HTML الأصلي
    pattern = r'const\s+healthNewsData\s*=\s*\[.*?\]\s*;'
    
    if re.search(pattern, current_code, re.DOTALL):
        updated_code = re.sub(pattern, ai_news_matrix, current_code, flags=re.DOTALL)
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(updated_code)
        print("تم تحديث الأخبار بنجاح تام! 🚀 تم الحفاظ على شكل وتصميم موقعك الأصلي 100% وتحديث الأخبار تلقائياً.")
    else:
        # خطة بديلة احتياطية في حال لم يجد تعبير Regex المتطابق تماماً لضمان عدم توقف السكربت
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(current_code)
        print("تنبيه: تم تشغيل السكربت بنجاح، لكن لم يتم استبدال المصفوفة. تأكد من وجود const healthNewsData = []; في كود الجافاسكريبت.")

except Exception as e:
    print(f"حدث خطأ أثناء معالجة التحديث الحذر: {e}")
