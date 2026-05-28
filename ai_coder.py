import google.generativeai as genai
import os
import re
import json

# 1. إعداد اتصال Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')
 
# 2. قراءة كود الموقع الحالي
try:
    with open("index.html", "r", encoding="utf-8") as f:
        html_code = f.read()
except FileNotFoundError:
    print("Error: index.html not found")
    exit(1)

# 3. طلب الأخبار من الـ AI
prompt = """
بصفتك خبير في الصحة العامة ومكافحة العدوى، قدم لي 3 أخبار طبية وصحية حديثة وموثوقة (مستجدات بكتيرية، أبحاث صحية، إرشادات وقائية).
يجب أن يكون الرد بتنسيق مصفوفة JSON فقط ومطابق تماماً لهذا الهيكل دون أي كلام جانبي أو علامات تشكيل كود برمجية زائدة:
[
  {
    "title": "عنوان الخبر الطبي الأول"،
    "content": "ملخص مهني دقيق ومختصر للخبر لفائدة الشباب المتصفحين."،
    "date": "16 مايو 2026"،
    "image": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=500"
  },
  {
    "title": "عنوان الخبر الطبي الثاني"،
    "content": "ملخص مهني وموجز للخبر الصحي الثاني..."،
    "date": "16 مايو 2026 Bey"،
    "image": "https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=500"
  },
  {
    "title": "عنوان الخبر الطبي الثالث"،
    "content": "ملخص مهني وموجز للخبر الصحي الثالث..." Train"،
    "date": "15 مايو 2026"،
    "image": "https://images.unsplash.com/photo-1532938911072-f1925345719a?w=500"
  }
]
"""

try:
    response = model.generate_content(prompt)
    json_match = re.search(r'\[.*\]', response.text, re.DOTALL)
    
    if json_match:
        news_data_string = json_match.group(0)
        
        # حقن مصفوفة الأخبار المحدثة داخل ملف الـ HTML
        news_script = f"const healthNewsData = {news_data_string};"
        updated_html = re.sub(r'const healthNewsData = \[.*?\];', news_script, html_code, flags=re.DOTALL)
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(updated_html)
            
        print("تم تحديث قسم الأخبار بنجاح عن طريق البوت التلقائي! 🚀")
    else:
        print("لم ينجح السكربت في استخراج مصفوفة الأخبار من الذكاء الاصطناعي.")

except Exception as e:
    print(f"حدث خطأ: {e}")
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
المطلوب في هذا التحديث:
1. إنشاء قسم "المصادر الموثوقة" يحتوي على أزرار سريعة تأخذ المستخدم إلى (PubMed, WHO Publications, CDC Infection Control).
2. إضافة جدول للأبحاث يحتوي على الأعمدة التالية: (اسم البحث، سنة النشر، المجال، رابط القراءة).
3. أضف 100 صفوف تجريبية لأبحاث حديثة اظهار خمسة ابحاث في كل مرة نضغط فيها زر عرض المزيد عن "جميع مجالات الصحة العامة".
4. تأكد من وجود زر "فلترة" بسيط للبحث داخل المكتبة.

المطلوب إصلاح أزرار "قراءة المزيد" في مكتبة الأبحاث:
1. تأكد أن كل زر "قراءة المزيد" يحتوي على رابط حقيقي (Link) لمصدر البحث.
2. استخدم روابط من موقع PubMed أو Google Scholar كمصادر افتراضية للأبحاث الحالية.
3. اجعل الرابط يفتح في "تبويب جديد" (target="_blank") لكي لا يخرج الزائر من موقعك.
4. إذا لم يتوفر رابط محدد، اجعل الزر يوجه المستخدم إلى محرك بحث PubMed مباشرة.


تطوير مكتبة الأبحاث بمحرك بحث ذكي
تطوير مكتبة الأبحاث الحالية عبر إنشاء نظام بحث ذكي ومتقدم يسمح للمستخدم بالوصول السريع والدقيق إلى الدراسات والمقالات العلمية. يعتمد النظام على تصنيف الأبحاث حسب التخصص، الكلمات المفتاحية، سنة النشر، نوع الدراسة، والموضوع الصحي، مع إمكانية البحث باللغة العربية والإنجليزية. كما يتضمن اقتراحات ذكية مرتبطة بموضوع البحث وعرض ملخصات مبسطة للأبحاث لتسهيل فهم المحتوى العلمي لغير المختصين. يهدف هذا التطوير إلى تعزيز تجربة المستخدم وتحويل المكتبة إلى مرجع علمي منظم وسهل الاستخدام للباحثين والمهتمين بالصحة العامة.
انشاء نظام إمكانية حفظ المقالات والنصائح الصحية والأبحاث المفضلة للرجوع إليها لاحقًا، بالإضافة إلى إنشاء قوائم مخصصة وتنظيم المحتوى حسب اهتمامات المستخدم. كما يتضمن النظام سجلًا للنشاطات الأخيرة، وإشعارات بالمحتوى الجديد المرتبط باهتمامات المستخدم، .
اضافة قسم اخر الاخبار الصحية المحلية والعالمية تتحدث تلقائيا وجعلها بعد قسم من نحن 
وازالة قسم التحقق من الشائعات 
- ممنوع كتابة أي كلمة خارج كود الـ HTML.
- ابدأ مباشرة بـ <!DOCTYPE html>.
- لا تكتب "إليك الكود" أو "بالتأكيد" أو أي شرح.
- لا تستخدم علامات الماركدوان مثل ```html.
الغاء ايقونة انشاء حساب. 
الغاء ايقونة التنبيهات والاشعارات.

بصفتك خبيراً متخصصاً في الصحة العامة ومكافحة العدوى والتحاليل الطبية المخبرية، قدم لي 3 أخبار طبية وصحية حديثة جداً وموثوقة ومثيرة لاهتمام المتصفحين والشباب.
ركز على مجالات: مقاومة البكتيريا للمضادات الحيوية، سلامة الأغذية، الصحة العامة الموجهة للوعي اليومي.

يجب أن يكون الرد بصيغة مصفوفة JSON فقط ومطابق تماماً لهذا الهيكل البرمجي دون أي نصوص تمهيدية، قفلات، أو علامات تشكيل الكود البرمجي الزائدة (مثل ```json):
[
  {
    "title": "عنوان الخبر الطبي الأول (مثال: مستجدات مقاومة الميكروبات للتعقيم)"،
    "content": "ملخص علمي دقيق، ومصاغ بأسلوب شيق ومبسط جداً وموجز في سطرين."،
    "date": "28 مايو 2026"،
    "category": "مكافحة العدوى"،
    "image": "[https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=500](https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=500)"
  },
  {
    "title": "عنوان الخبر الثاني (يمس التغذية أو سلامة الغذاء)"،
    "content": "ملخص توعوي موجز ودقيق وشيق في سطرين لتنبيه المتصفحين..."،
    "date": "28 مايو 2026"،
    "category": "سلامة الأغذية"،
    "image": "[https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=500](https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=500)"
  },
  {
    "title": "عنوان الخبر الثالث (صحة عامة أو عادات يومية خطيرة)"،
    "content": "ملخص علمي تفاعلي سريع وموجه للشباب لحمايتهم..."،
    "date": "27 مايو 2026"،
    "category": "صحة عامة"،
    "image": "[https://images.unsplash.com/photo-1532938911072-f1925345719a?w=500](https://images.unsplash.com/photo-1532938911072-f1925345719a?w=500)"
  }
]


try:
    response = model.generate_content(prompt)
    json_match = re.search(r'\[.*\]', response.text, re.DOTALL)
    
    if json_match:
        news_data_string = json_match.group(0)
        
        # استبدال مصفوفة الأخبار الفارغة بالمصفوفة الذكية الجديدة التي تم توليدها
        news_script = f"const healthNewsData = {news_data_string};"
        updated_html = re.sub(r'const healthNewsData = \[.*?\];', news_script, html_code, flags=re.DOTALL)
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(updated_html)
            
        print("تمت عملية جلب الأخبار وحقنها في كود الموقع الأصلي بنجاح تام! 🚀")
    else:
        print("خطأ برمي: لم ينجح السكربت في عزل مصفوفة الأخبار من استجابة الـ AI.")

except Exception as e:
    print(f"حدث خطأ أثناء الاتصال أو تحديث البيانات: {e}")


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
