import google.generativeai as genai
import os
import re
import json
from datetime import datetime

# 1. إعداد الاتصال بجيمني
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

# 2. جلب تاريخ اليوم الحالي ديناميكياً
current_date_str = datetime.now().strftime("%Y-%m-%d")

# 3. قراءة ملف الموقع الحالي
try:
    with open("index.html", "r", encoding="utf-8") as f:
        current_code = f.read()
except FileNotFoundError:
    print("خطأ: لم يتم العثور على ملف index.html في المسار الحالي.")
    exit(1)

# 4. برومبت ذكي مخصص فقط للأخبار بدون المساس بشكل وتصميم الموقع
prompt = f"""
أنت مبرمج محترف. المطلوب منك فقط هو توليد بيانات مصفوفة الأخبار الطبية لتاريخ اليوم وهو ({current_date_str}).
يجب أن تركز الأخبار على مجالات: مقاومة المضادات الحيوية، سلامة الأغذية، ومكافحة العدوى في المختبرات الطبية والصحة العامة.

شروط صارمة للبيانات:
1. قم بإنشاء 3 أخبار حقيقية وموثوقة ومحدثة.
2. لا تضع حقل للتاريخ نهائياً في البيانات.
3. يجب وضع رابط صورة مباشر، عالي الجودة وشغال 100% من Unsplash يعبر بدقة دلالية عن محتوى الخبر (مثل صور بكتيريا، أطباء، مختبرات، أطعمة صحية). ممنوع ترك الصورة فارغة.

أريدك أن ترسل لي كود المصفوفة فقط بصيغة جافاسكريبت نقي (Pure JavaScript Array) باسم `healthNewsData` كالتالي تماماً:
const healthNewsData = [
  {{
    id: 1,
    title: "عنوان الخبر الأول المثير والحديث",
    description: "تفاصيل الخبر الأول بدقة علمية لغير المختصين والمستند لمصادر موثوقة.",
    image: "https://images.unsplash.com/..."
  }},
  ...
];

ممنوع كتابة أي مقدمات أو شروحات أو استخدام علامات الماركدوان الزائدة مثل ```javascript، ابدأ بكتابة const وانته بـ ]; فوراً.
"""

print(f"جاري طلب الأخبار الحية المحدثة لليوم {current_date_str}... ⏳")

try:
    response = model.generate_content(prompt)
    ai_news_matrix = response.text.strip()
    
    # تنظيف مخرجات الـ AI للتأكد من أنها مصفوفة صافية
    if "```" in ai_news_matrix:
        ai_news_matrix = re.sub(r'```javascript\n|```html\n|```', '', ai_news_matrix).strip()

    # 5. استبدال مصفوفة الأخبار القديمة بالجديدة داخل كود الموقع الأصلي دون تغيير التصميم!
    # البحث عن المصفوفة القديمة واستبدالها بالكامل بذكاء
    pattern = r'const\s+healthNewsData\s*=\s*\[.*?\]\s*;'
    
    if re.search(pattern, current_code, re.DOTALL):
        updated_code = re.sub(pattern, ai_news_matrix, current_code, flags=re.DOTALL)
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(updated_code)
        print("تم تحديث الأخبار بنجاح تام! 🚀 تم الحفاظ على شكل وتصميم موقعك الأصلي 100% وتعديل المصفوفة فقط.")
    else:
        print("خطأ: لم نجد مصفوفة باسم const healthNewsData = []; داخل ملف index.html الحالي للاستبدال.")
        print("تأكد من وجود المصفوفة بهذا الاسم في كود الجافاسكريبت الخاص بموقعك الأصلي.")

except Exception as e:
    print(f"حدث خطأ أثناء معالجة التحديث الحذر: {e}")
