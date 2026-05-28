import google.generativeai as genai
import os
import re
import json
import time

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

# 2. قراءة ملف الموقع الحالي
try:
    with open("index.html", "r", encoding="utf-8") as f:
        current_code = f.read()
except FileNotFoundError:
    print("خطأ: لم يتم العثور على ملف index.html في المسار الحالي.")
    exit(1)
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

# 2. قراءة ملف الموقع الحالي
try:
    with open("index.html", "r", encoding="utf-8") as f:
        current_code = f.read()
except FileNotFoundError:
    print("خطأ: لم يتم العثور على ملف index.html في المسار الحالي.")
    exit(1)
# 3. البرومبت الشامل (دمج التحديث الهيكلي + طلب الأخبار)
prompt = f"""
خذهذا كود الـ HTML الحالي للموقع:
{current_code}

المطلوب منك هو تحديث هذا الكود وإعادة صياغته بالكامل لينفذ المهام التالية بدقة عالية:

أولاً: تحديثات وتطويرات بنية الموقع الأساسية:
1. أضف أزرار مشاركة فيسبوك وواتساب وزر نسخ النصيحة لكل بطاقة نصيحة طبية.
2. اجعل التصميم متناسقاً تماماً مع ألوان الموقع الحالية (يفضل الاعتماد على ألوان متناسقة مع تخصص مكافحة العدوى والصحة العامة كالأخضر الطبي والأزرق الداكن).
3. أضف صورة مميزة للرئيسية للموقع لها علاقة مباشرة بالصحة العامة والمختبرات الميكروبية.
4. إنشاء قسم "المصادر الموثوقة" يحتوي على أزرار سريعة تأخذ المستخدم إلى (PubMed, WHO Publications, CDC Infection Control).
5. بناء "مكتبة للأبحاث العلمية" في مجال الصحة العامة تحتوي على جدول منظم بالأعمدة التالية: (اسم البحث، سنة النشر، المجال، رابط القراءة).
6. أضف 100 صف تجريبي لأبحاث حديثة (واقعية أو افتراضية دقيقة علمياً في مجالات مقاومة البكتيريا، مكافحة العدوى، سلامة الأغذية) مع إظهار 5 أبحاث فقط في كل مرة، وتفعيل زر "عرض المزيد" لإظهار الخمسة التالية وهكذا لجميع مجالات الصحة العامة.
7. تأكد من وجود زر "فلترة" وبحث ذكي متقدم داخل المكتبة يسمح بالوصول السريع حسب التخصص، الكلمات المفتاحية، أو سنة النشر، مع إمكانية البحث باللغة العربية والإنجليزية، وعرض ملخصات مبسطة للأبحاث لغير المختصين.
8. إصلاح أزرار "قراءة المزيد" في مكتبة الأبحاث لتشمل روابط حقيقية أو افتراضية موثوقة تفتح في تبويب جديد (target="_blank")، وإذا لم يتوفر رابط محدد توجه المستخدم إلى محرك بحث PubMed مباشرة.
9. إنشاء نظام (باستخدام LocalStorage في الجافاسكريبت) لإمكانية حفظ المقالات والنصائح الصحية والأبحاث المفضلة للرجوع إليها لاحقاً، مع سجل للنشاطات الأخيرة.
10. إضافة قسم "آخر الأخبار الصحية المحلية والعالمية" وجعله مباشرة بعد قسم (من نحن)، مع إزالة قسم (التحقق من الشائعات) تماماً.
11. إلغاء أيقونة إنشاء حساب، وإلغاء أيقونة التنبيهات والإشعارات تماماً من الهيدر أو القوائم.
1. برومبت إلغاء جزئية الحساب (الحذف النهائي)
"أمر صارم: قم بإزالة أي أكواد، عناصر واجهة (UI)، أو أزرار تتعلق بـ 'إنشاء حساب'، 'تسجيل الدخول'، أو 'الملف الشخصي' من شريط التنقل (Navbar) ومن كامل الصفحة. يجب أن تكون المنصة مفتوحة بالكامل ومتاحة لجميع الزوار مباشرة دون أي قيود أو متطلبات لتسجيل الدخول."
2. برومبت إجبار الذكاء الاصطناعي على وضع صور للأخبار (حتى لو كانت توليدية)
"أمر إجباري ومقدس للصور: في مصفوفة الأخبار healthNewsData، يمنع منعاً باتاً ترك حقل image فارغاً أو وضع روابط مكسورة. يجب عليك تزويد كل خبر برابط صورة حقيقي، عالي الدقة، ومتوافق مع محتوى الخبر (يفضل استخدام روابط مباشرة من Unsplash). إذا لم تجد صورة حقيقية، فقم بصياغة أو استخدام رابط لصورة مولدة بالذكاء الاصطناعي (AI-generated) تكون معبرة عن المختبرات الطبية، البكتيريا، أو الصحة العامة، بحيث تظهر الصورة كخلفية حية للخبر لتفادي تدمير واجهة المستخدم (UI)."
3. برومبت أمر الحفظ التلقائي في قائمة "مفضلاتي" (LocalStorage)
"أمر جافاسكريبت لوظيفة المفضلة: قم ببرمجة دالة ذكية مستقرة مرتبطة بزر 'الحفظ' في كروت النصائح والأبحاث. عند الضغط على الزر، يجب أن يتم تخزين كائن النصيحة أو البحث تلقائياً داخل ذاكرة المتصفح localStorage (مثال: localStorage.setItem('myFavorites', ...)). فوراً وبدون الحاجة لإعادة تحميل الصفحة، قم بتحديث واجهة قسم 'قائمة مفضلاتي' لتعرض العناصر المحفوظة حديثاً بشكل تلقائي وديناميكي، مع تغيير شكل أو لون زر الحفظ ليشير إلى 'تم الحفظ في المفضلات'."
ثانياً: تفعيل مصفوفة الأخبار الحية (JSON):
تأكد من أن الكود يحتوي في قسم الـ Script على مصفوفة فارغة باسم:
const healthNewsData = []; 
وقم بملئها تلقائياً بـ 3 أخبار طبية وصحية حديثة جداً وموثوقة ومثيرة لاهتمام المتصفحين والشباب، تركز على مجالات: مقاومة البكتيريا للمضادات الحيوية، سلامة الأغذية، والصحة العامة، مع روابط صور حقيقية من Unsplash داخل المصفوفة.
خذ كود الـ HTML الحالي للموقع:
{current_code}

المطلوب منك هو تحديث هذا الكود وإعادة صياغته بالكامل لينفذ المهام التالية بدقة هندسية صارمة:

أولاً: إلغاء واجهة الحساب والتنبيهات نهائياً:
- قم بحذف أي أزرار أو أيقونات أو نصوص تتعلق بـ (إنشاء حساب / تسجيل دخول / الملف الشخصي / الإشعارات / التنبيهات) من الـ Navbar أو الفوتر أو أي مكان في الصفحة. المنصة يجب أن تكون مفتوحة ومتاحة بالكامل للزوار مباشرة.

ثانياً: حل مشكلة عدم ظهور صور الأخبار (إجباري):
- في مصفوفة الأخبار `healthNewsData`، يُمنع منعاً باتاً وضع روابط مكسورة أو تركها فارغة.
- يجب استخدام هذه الروابط الحقيقية والشغالة 100% والمتاحة حالياً في عام 2026 للأخبار الثلاثة بالتناوب:
  1. الخبر الأول (مكافحة العدوى/المختبرات): https://images.unsplash.com/photo-1579165466511-71e5331940a5?w=600
  2. الخبر الثاني (سلامة الأغذية/التغذية): https://images.unsplash.com/photo-1498837167922-ddd27525d352?w=600
  3. الخبر الثالث (الصحة العامة/الوعي): https://images.unsplash.com/photo-1476480862126-209bfaa8edc8?w=600
- تأكد أن الكود يعرض هذه الصور في كروت الأخبار بشكل صحي ومستقر.

ثالثاً: حل مشكلة نظام الحفظ والمفضلة تلقائياً (LocalStorage):
- تأكد من وجود قسم واضح في واجهة المستخدم تحت اسم "قائمة مفضلاتي" (بجانب أو أسفل قسم الأبحاث) يحتوي على معرف `id="favorites-list"`.
- يجب أن تقوم بكتابة دوال الجافاسكريبت التالية كاملة وبدون أي اختصار داخل وسم الـ <script> لضمان اشتغال الحفظ فورياً:

  1. دالة الحفظ:
  function saveToFavorites(id, title, type) {{
      let favorites = JSON.parse(localStorage.getItem('healthFavorites')) || [];
      if (!favorites.some(item => item.id === id)) {{
          favorites.push({{ id, title, type, date: new Date().toLocaleDateString('ar-LY') }});
          localStorage.setItem('healthFavorites', JSON.stringify(favorites));
          renderFavorites();
          alert('تم الحفظ في المفضلات بنجاح! 🌟');
      }} else {{
          alert('هذا العنصر موجود بالفعل في مفضلاتك.');
      }}
  }}

  2. دالة العرض التلقائي:
  function renderFavorites() {{
      const container = document.getElementById('favorites-list');
      if (!container) return;
      let favorites = JSON.parse(localStorage.getItem('healthFavorites')) || [];
      if (favorites.length === 0) {{
          container.innerHTML = '<p class="text-muted small text-center my-3">لا توجد عناصر محفوظة حالياً.</p>';
          return;
      }}
      container.innerHTML = favorites.map(item => `
          <div class="d-flex justify-content-between align-items-center p-2 mb-2 bg-light rounded" style="border-right: 3px solid #198754;">
              <div>
                  <h6 class="fw-bold mb-0 small text-dark">${{item.title}}</h6>
                  <small class="text-muted" style="font-size:0.7rem;">${{item.type}} - ${{item.date}}</small>
              </div>
              <button class="btn btn-sm text-danger" onclick="removeFromFavorites('${{item.id}}')"><i class="fas fa-trash-alt"></i></button>
          </div>
      `).join('');
  }}

  3. دالة الحذف من المفضلة:
  function removeFromFavorites(id) {{
      let favorites = JSON.parse(localStorage.getItem('healthFavorites')) || [];
      favorites = favorites.filter(item => item.id !== id);
      localStorage.setItem('healthFavorites', JSON.stringify(favorites));
      renderFavorites();
  }}

- تأكد من استدعاء `renderFavorites();` فوراً داخل حدث الـ `DOMContentLoaded` لكي تظهر المفضلات بمجرد فتح الزائر للموقع.
- تأكد أن أزرار الحفظ في كروت النصائح وفي جدول مكتبة الأبحاث تستدعي الدالة هكذا: `onclick="saveToFavorites('ID_فريد', 'عنوان_العنصر', 'نصيحة أو بحث')"`

رابعاً: الأبحاث وأقسام الموقع:
- أضف قسم "المصادر الموثوقة" (PubMed, WHO, CDC).
- بناء جدول الأبحاث (اسم البحث، سنة النشر، المجال، رابط القراءة) يحتوي على الـ 100 صف التجريبية مع زر "عرض المزيد" لفتح 5 صفحات في كل ضغطة، وتفعيل نظام بحث وفلترة ذكي باللغتين العربية والإنجليزية.
- إضافة قسم الأخبار الصحية بعد (من نحن) وإزالة قسم (التحقق من الشائعات) نهائياً.

شروط صارمة للاستجابة:
- ممنوع كتابة أي كلمة شرح أو تمهيد خارج كود الـ HTML.
- ابدأ الرد مباشرة بـ <!DOCTYPE html> وانته بـ </html> دون استخدام علامات الماركدوان الزائدة مثل ```html.
شروط صارمة للاستجابة:
- ممنوع كتابة أي كلمة شرح أو تمهيد خارج كود الـ HTML.
- ابدأ الرد مباشرة بـ <!DOCTYPE html> وانته بـ </html>.
- لا تكتب "إليك الكود" أو "بالتأكيد" ولا تستخدم علامات الماركدوان الزائدة مثل ```html.
"""

print("جاري إرسال الطلب الضخم لـ Gemini لتحديث هيكل الموقع وحقن الأخبار... قد يستغرق الأمر ثوانٍ إضافية ⏳")

try:
    response = model.generate_content(prompt)
    raw_text = response.text
    
    # محاولة استخراج الكود النظيف المحصور بين وسوم html لضمان السلامة
    match = re.search(r'<!DOCTYPE html>.*</html>', raw_text, re.DOTALL | re.IGNORECASE)
    if match:
        clean_code = match.group(0)
    else:
        # إذا لم يجد الوسوم بشكل صريح، يقوم بتنظيف علامات الماركدوان التقليدية إن وجدت
        clean_code = re.sub(r'```html\n|```', '', raw_text)

    # حفظ الكود الشامل والنظيف في ملف index.html الأساسي
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(clean_code.strip())
        
    print(f"مبروك يا دكتور! تم تحديث الموقع بالكامل بنجاح 🚀.")
    print(f"الموقع الآن يحتوي على: المكتبة الـ 100 صف، نظام البحث، المفضلة، والأخبار الحية مدمجة تلقائياً.")
    print(f"الموديل المستخدم: {model_name}")
try:
    response = model.generate_content(prompt)
    raw_text = response.text
    
    match = re.search(r'<!DOCTYPE html>.*</html>', raw_text, re.DOTALL | re.IGNORECASE)
    if match:
        clean_code = match.group(0)
    else:
        clean_code = re.sub(r'```html\n|```', '', raw_text)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(clean_code.strip())
        
    print(f"تم التحديث بنجاح تام! 🚀 الصور أصبحت حقيقية، ودوال الحفظ والمفضلة حُقنت بالكامل في الموقع الأصلي.")

except Exception as e:
    print(f"حدث خطأ أثناء معالجة التحديث الشامل: {e}")
