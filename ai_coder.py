import google.generativeai as genai
import os
import re

# 1. إعداد الاتصال بجيمني
# Ensure the GEMINI_API_KEY environment variable is set.
# Example: export GEMINI_API_KEY='YOUR_API_KEY'
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
except Exception as e:
    print(f"Error configuring Gemini API: {e}")
    print("Please ensure the GEMINI_API_KEY environment variable is set.")
    exit() # Exit if API key is not configured

# 2. اختيار الموديل المتاح تلقائياً
# Attempts to find a suitable model that supports 'generateContent'.
# Falls back to 'gemini-1.5-flash' if no other suitable model is found or an error occurs.
model_name = 'gemini-1.5-flash'
try:
    available_models = genai.list_models()
    for m in available_models:
        if 'generateContent' in m.supported_generation_methods:
            model_name = m.name
            print(f"Using model: {model_name}")
            break
except Exception as e:
    print(f"Could not list models, falling back to default: {model_name}. Error: {e}")
    model_name = 'models/gemini-1.5-flash' # Explicitly use the full path if needed

model = genai.GenerativeModel(model_name)

# 3. قراءة ملف الموقع الحالي أو تهيئة محتوى افتراضي
# Reads the existing index.html file. If it doesn't exist, it initializes current_code
# with a placeholder message to indicate a new project or missing file.
try:
    with open("index.html", "r", encoding="utf-8") as f:
        current_code = f.read()
    print("Successfully read existing index.html")
except FileNotFoundError:
    current_code = "<!-- index.html not found, generating new content -->"
    print("index.html not found. A new file will be generated.")
except Exception as e:
    print(f"Error reading index.html: {e}")
    current_code = f"<!-- Error reading index.html: {e} -->"

# --- Prompt Construction ---
# This section defines the instructions for the AI model.
# It combines multiple requests for website development and content generation.

# Firebase Configuration - Placeholder for user's actual config
# IMPORTANT: Replace the placeholder values with your actual Firebase project credentials.
# This configuration is essential for Firebase authentication and other services.
firebase_config_placeholder = """
const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_AUTH_DOMAIN",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_STORAGE_BUCKET",
  messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
  appId: "YOUR_APP_ID"
};
"""

# Combined prompt incorporating all requirements:
# - Initial prompt for social buttons, design, image, and research library.
# - Second prompt for full HTML rewrite with Tailwind CSS, Firebase Auth, login/signup.
# - Third prompt for detailed Firebase Auth implementation (modal, JS functions, error handling).
# - Fourth prompt for advanced research library search.
# - Fifth prompt for integrated user accounts (saving favorites, history, notifications).
# - Sixth prompt for adding a news section and removing a rumor check section.
# - Strict output format requirements (HTML only, no extra text, specific start/end).

prompt = f"""
أعد كتابة ملف index.html بالكامل لموقع "أثر صحي" (Impact Health).

المواصفات المطلوبة:
1.  **التصميم العام:** تصميم احترافي باستخدام Tailwind CSS، مع الحفاظ على الألوان الخضراء والطبية المميزة للموقع.
2.  **نظام الحسابات الشخصية:**
    *   تفعيل نظام الحسابات باستخدام Firebase Auth (Modular SDK).
    *   إضافة مكتبات Firebase (App و Auth) في قسم الـ Head.
    *   إضافة "نافذة منبثقة" (Modal) احترافية تظهر عند الضغط على زر "تسجيل الدخول" في القائمة العلوية.
    *   برمجة وظائف JavaScript للقيام بـ (إنشاء حساب جديد، تسجيل دخول، تسجيل خروج) باستخدام `createUserWithEmailAndPassword` و `signInWithEmailAndPassword`.
    *   ربط أزرار "إنشاء حساب جديد" و "تسجيل الدخول" في النافذة المنبثقة بوظائف Firebase المناسبة.
    *   إضافة كود JavaScript لإغلاق النافذة المنبثقة بعد نجاح الدخول وإظهار تنبيه (Success Message).
    *   إضافة معالجة للأخطاء (مثلاً: إذا كانت كلمة المرور ضعيفة أو الإيميل مستخدم مسبقاً) لتظهر للمستخدم.
    *   تأكد من أن الموقع يغير زر "تسجيل الدخول" إلى "الملف الشخصي" أو "خروج" بعد نجاح العملية.
    *   توفير مكان واضح لوضع 'firebaseConfig' الخاص بي في الكود، مع استخدام متغير `firebaseConfig` المعرف أدناه.
    *   النظام يتيح للمستخدم إنشاء ملف شخصي خاص به للوصول إلى تجربة استخدام أكثر تنظيمًا وتفاعلية.
    *   إمكانية حفظ المقالات والنصائح الصحية والأبحاث المفضلة للرجوع إليها لاحقًا.
    *   إنشاء قوائم مخصصة وتنظيم المحتوى حسب اهتمامات المستخدم.
    *   يتضمن سجلًا للنشاطات الأخيرة.
    *   إشعارات بالمحتوى الجديد المرتبط باهتمامات المستخدم.
    *   اقتراحات ذكية مبنية على تفاعله داخل المنصة.
    *   تلقي تنبيهات عند إضافة أبحاث أو تحديثات جديدة.

3.  **أزرار التنقل الرئيسية:**
    *   إضافة أزرار "تسجيل الدخول" و "إنشاء حساب" في الأعلى (والتي ستفتح النافذة المنبثقة).
    *   بعد تسجيل الدخول، يجب أن يتغير زر "تسجيل الدخول" إلى "الملف الشخصي" أو "خروج".

4.  **قسم "المصادر الموثوقة":**
    *   إنشاء قسم "المصادر الموثوقة" يحتوي على أزرار سريعة تأخذ المستخدم إلى (PubMed, WHO Publications, CDC Infection Control).

5.  **مكتبة الأبحاث:**
    *   **التطوير الأساسي:**
        *   إضافة جدول للأبحاث يحتوي على الأعمدة التالية: (اسم البحث، سنة النشر، المجال، رابط القراءة).
        *   إضافة 100 صفوف تجريبية لأبحاث حديثة.
        *   إظهار خمسة أبحاث في كل مرة عند الضغط على زر "عرض المزيد" عن "جميع مجالات الصحة العامة".
        *   تأكد من وجود زر "فلترة" بسيط للبحث داخل المكتبة.
    *   **إصلاح أزرار "قراءة المزيد":**
        *   تأكد أن كل زر "قراءة المزيد" يحتوي على رابط حقيقي (Link) لمصدر البحث.
        *   استخدم روابط من موقع PubMed أو Google Scholar كمصادر افتراضية للأبحاث الحالية.
        *   اجعل الرابط يفتح في "تبويب جديد" (target="_blank").
        *   إذا لم يتوفر رابط محدد، اجعل الزر يوجه المستخدم إلى محرك بحث PubMed مباشرة.
    *   **محرك بحث ذكي ومتقدم:**
        *   نظام بحث يسمح بالوصول السريع والدقيق للدراسات والمقالات العلمية.
        *   تصنيف الأبحاث حسب التخصص، الكلمات المفتاحية، سنة النشر، نوع الدراسة، والموضوع الصحي.
        *   إمكانية البحث باللغة العربية والإنجليزية.
        *   يتضمن اقتراحات ذكية مرتبطة بموضوع البحث.
        *   عرض ملخصات مبسطة للأبحاث لتسهيل فهم المحتوى العلمي لغير المختصين.

6.  **قسم الأخبار:**
    *   إضافة قسم "آخر الأخبار الصحية المحلية والعالمية" يتحدث تلقائياً (إذا كان ذلك ممكناً عبر API أو مصدر خارجي، وإلا فسيتم وضع محتوى تجريبي).
    *   يجب أن يكون هذا القسم بعد قسم "من نحن".
    *   إزالة قسم "التحقق من الشائعات".

7.  **ميزات إضافية:**
    *   إضافة صورة للرئيسية للموقع لها علاقة بالمحتوى.
    *   إضافة أزرار مشاركة فيسبوك وواتساب وزر نسخ النصيحة لكل بطاقة نصيحة (إذا كانت هناك بطاقات نصائح موجودة في الكود الحالي أو سيتم إنشاؤها).

**متطلبات تنسيق الإجابة:**
*   أجب بكود HTML كامل فقط يبدأ بـ `<!DOCTYPE html>` وينتهي بـ `</html>`.
*   ممنوع كتابة أي كلمة خارج كود الـ HTML.
*   لا تكتب "إليك الكود" أو "بالتأكيد" أو أي شرح إضافي.
*   لا تستخدم علامات الماركدوان مثل ```html.
*   تأكد أن الكود كامل (Complete) ولا يحتوي على أخطاء برمجية واضحة.

**الكود الحالي (للمرجع فقط، سيتم إعادة كتابة الملف بالكامل):**
```
{current_code}
```

**إعدادات Firebase (استخدم هذا المتغير في الكود):**
{firebase_config_placeholder}
"""

# 5. التنفيذ وطلب الكود وتنظيفه
try:
    print("Generating content from AI model...")
    response = model.generate_content(prompt)
    raw_text = response.text
    
    # محاولة استخراج الكود فقط بين وسوم html لضمان النظافة
    # This regex attempts to find the complete HTML document from <!DOCTYPE html> to </html>.
    match = re.search(r'<!DOCTYPE html>.*</html>', raw_text, re.DOTALL | re.IGNORECASE)
    if match:
        clean_code = match.group(0)
        print("Extracted HTML code using regex.")
    else:
        # If the full HTML tags are not found, it tries to remove common markdown code block delimiters.
        clean_code = re.sub(r'```html\n|```', '', raw_text).strip()
        print("Could not find full HTML tags, attempting to clean markdown.")

    # 6. حفظ الكود النظيف في الملف
    # Writes the cleaned HTML code to index.html.
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(clean_code)
    print("DONE: Website rebuilt with full Authentication and Research Library features.")

except Exception as e:
    print(f"Final Attempt Error: {e}")
    print("Failed to generate or save the website code.")


