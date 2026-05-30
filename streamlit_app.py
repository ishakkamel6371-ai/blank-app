import streamlit as 
import streamlit as st
from google import genai
from PIL import Image

# إعدادات الواجهة
st.set_page_config(page_title="محلل الأسهم الذكي", page_icon="📈", layout="centered")

st.title("📈 مستشارك المالي الذكي")
st.write("ارفع لقطة شاشة (Screenshot) للمنحنى البياني من تطبيق ثاندر لتبدأ التحليل الفني فوراً.")

# خانة إدخال مفتاح الـ API لـ Gemini
api_key = st.text_input("🔑 أدخل مفتاح Gemini API الخاص بك:", type="password")

if api_key:
    try:
        # ربط التطبيق بذكاء Gemini الاصطناعي
        client = genai.Client(api_key=api_key)
        
        # خانة رفع الصور
        uploaded_file = st.file_uploader("📸 اختر صورة المنحنى من الاستوديو:", type=["jpg", "jpeg", "png"])
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="الصورة المرفوعة من ثاندر", use_container_width=True)
            
            if st.button("🧐 ابدأ التحليل الفني الآن"):
                with st.spinner("جاري قراءة المنحنى وتحليله بواسطة الذكاء الاصطناعي..."):
                    prompt = (
                        "أنت محلل فني خبير ومستشار مالي لأسواق الأسهم. انظر إلى صورة المنحنى البياني المرفقة "
                        "(من تطبيق تداول الأسهم ثاندر)، وحلل حركة السعر الموضحة. حدد اتجاه السهم الحالي (صاعد/هابط/عرضي)، "
                        "واستخرج نقاط الدعم والمقاومة التقريبية، ثم قدم توصية استثمارية واضحة ومبسطة للمبتدئين (شراء / بيع / انتظار) مع ذكر الأسباب."
                    )
                    # توليد التقرير
                    response = client.models.generate_content(model='gemini-2.5-flash', contents=[prompt, image])
                    st.subheader("🤖 تقرير الخبير الذكي:")
                    st.markdown(response.text)
    except Exception as e:
        st.error(f"حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {e}")
else:
    st.info("⚠️ يرجى كتابة مفتاح Gemini API في الخانة بالأعلى لتفعيل خدمات التحليل وقراءة الصور.")
