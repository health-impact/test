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

import google.generativeai as genai
import os

# 1. إعداد الاتصال
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. بيانات Firebase الحقيقية (الخاصة بك)
firebase_config = """
const firebaseConfig = {
  apiKey: "AIzaSyAz-mbnZhssLbV4-AOYz4KzqvORphN-PNw",
  authDomain: "atharsehi.firebaseapp.com",
  projectId: "atharsehi",
  storageBucket: "atharsehi.firebasestorage.app",
  messagingSenderId: "1020303874414",
  appId: "1:1020303874414:web:4f8a65e51952aeb8b5497f"
};
"""

# 3. محاولة قراءة الكود الحالي أو بناء واحد جديد
try:
    with open("index.html", "r", encoding="utf-8") as f:
        current_code = f.read()
except:
    current_code = "New Project"

# 4. طلب البناء الكامل
prompt = f"""
أعد كتابة ملف index.html بالكامل لموقع "أثر صحي" (Impact Health).
المواصفات المطلوبة:
1. تصميم احترافي بـ Tailwind CSS (نفس الألوان الخضراء والطبية).
2. تفعيل نظام الحسابات باستخدام هذا الكود: {firebase_config}
3. إضافة أزرار "تسجيل الدخول" و "إنشاء حساب" في الأعلى.
4. برمج الأزرار باستخدام Firebase Auth (Modular SDK) لتعمل فعلياً.
5. أضف قسم "حسابة المعقمات" و "مكتبة الأبحاث" بشكل مبسط.
6. تأكد أن الكود كامل (Complete) ولا يحتوي على أخطاء برمجية.

أجب بكود HTML فقط يبدأ بـ <!DOCTYPE html> وينتهي بـ </html>.
"""

# 5. التنفيذ والحفظ الإجباري
try:
    response = model.generate_content(prompt)
    full_html = response.text
    
    # تنظيف الرد من أي كلام جانبي
    if "<!DOCTYPE html>" in full_html:
        start = full_html.find("<!DOCTYPE html>")
        end = full_html.rfind("</html>") + 7
        clean_html = full_html[start:end]
    else:
        clean_html = full_html.replace("```html", "").replace("```", "").strip()

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(clean_html)
    print("DONE: Website rebuilt with full Authentication.")
except Exception as e:
    print(f"Final Attempt Error: {e}")
المطلوب تفعيل نظام الحسابات الشخصية بشكل كامل: 
1. أضف مكتبات Firebase (App و Auth) في قسم الـ Head.
2. أضف "نافذة منبثقة" (Modal) احترافية تظهر عند الضغط على زر "تسجيل الدخول" في القائمة العلوية.
3. برمج وظائف JavaScript للقيام بـ (إنشاء حساب جديد، تسجيل دخول، تسجيل خروج).
4. تأكد من أن الموقع يغير زر "تسجيل الدخول" إلى "الملف الشخصي" أو "خروج" بعد نجاح العملية.
5. اترك تعليقاً واضحاً في الكود يوضح أين أضع firebaseConfig الخاص بي.
المشكلة: أزرار "تسجيل الدخول" و "إنشاء حساب" في النافذة المنبثقة لا تعمل.
المطلوب إصلاحه :   
1. ربط زر "إنشاء حساب جديد" بوظيفة Firebase (createUserWithEmailAndPassword).
2. ربط زر "تسجيل الدخول" بوظيفة Firebase (signInWithEmailAndPassword).
3. إضافة كود JavaScript لإغلاق النافذة المنبثقة بعد نجاح الدخول وإظهار تنبيه (Success Message).
4. تأكد من وجود مكان واضح لوضع 'firebaseConfig' الخاص بي في الكود.
5. إضافة معالجة للأخطاء (مثلاً: إذا كانت كلمة المرور ضعيفة أو الإيميل مستخدم مسبقاً) لتظهر للمستخدم.
تطوير مكتبة الأبحاث بمحرك بحث ذكي
تطوير مكتبة الأبحاث الحالية عبر إنشاء نظام بحث ذكي ومتقدم يسمح للمستخدم بالوصول السريع والدقيق إلى الدراسات والمقالات العلمية. يعتمد النظام على تصنيف الأبحاث حسب التخصص، الكلمات المفتاحية، سنة النشر، نوع الدراسة، والموضوع الصحي، مع إمكانية البحث باللغة العربية والإنجليزية. كما يتضمن اقتراحات ذكية مرتبطة بموضوع البحث وعرض ملخصات مبسطة للأبحاث لتسهيل فهم المحتوى العلمي لغير المختصين. يهدف هذا التطوير إلى تعزيز تجربة المستخدم وتحويل المكتبة إلى مرجع علمي منظم وسهل الاستخدام للباحثين والمهتمين بالصحة العامة.
انشاء نظام حسابات شخصية متكامل داخل المنصة ويكون في بداية الموق بعد قسم من نحن يتيح للمستخدم إنشاء ملف شخصي خاص به للوصول إلى تجربة استخدام أكثر تنظيمًا وتفاعلية. يوفّر النظام إمكانية حفظ المقالات والنصائح الصحية والأبحاث المفضلة للرجوع إليها لاحقًا، بالإضافة إلى إنشاء قوائم مخصصة وتنظيم المحتوى حسب اهتمامات المستخدم. كما يتضمن النظام سجلًا للنشاطات الأخيرة، وإشعارات بالمحتوى الجديد المرتبط باهتمامات المستخدم، واقتراحات ذكية مبنية على تفاعله داخل المنصة و تلقي تنبيهات عند إضافة أبحاث أو تحديثات جديدة.
اضافة قسم اخر الاخبار الصحية المحلية والعالمية تتحدث تلقائيا وجعلها بعد قسم من نحن  
وازالة قسم التحقق من الشائعات 
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
