
import streamlit as st
from google import genai
from PIL import Image

# 1. إعدادات الصفحة والواجهة الاحترافية
st.set_page_config(
    page_title="مستشارك المالي الذكي برو", 
    page_icon="📊", 
    layout="centered"
)

# تحسين المظهر العام باستخدام CSS بسيط لجعله مناسباً للموبايل
st.markdown("""
    <style>
    .main { text-align: right; direction: rtl; }
    div.stButton > button:first-child {
        background-color: #009688;
        color: white;
        border-radius: 8px;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 مستشارك المالي الذكي (نسخة برو)")
st.write("مرحباً بك! منصتك الشاملة لتحليل أسهم البورصة المصرية والعالمية باستخدام الذكاء الاصطناعي.")

# 2. إدارة مفتاح الـ API بأمان وسهولة
api_key = st.text_input("🔑 أدخل مفتاح Gemini API الخاص بك لتفعيل المنصة:", type="password")

if api_key:
    try:
        client = genai.Client(api_key=api_key)
        
        # إنشاء تبويبين (Tabs) لتقسيم التطبيق بشكل احترافي ومنظم
        tab1, tab2, tab3 = st.tabs(["📸 تحليل صور ثاندر", "💬 اسأل المستشار المالي", "🧮 حاسبة المستثمر"])
        
        # --- التبويب الأول: تحليل الصور الفني ---
        with tab1:
            st.subheader("تحليل المنحنيات والشموع اليابانية")
            uploaded_file = st.file_uploader("اختر صورة المنحنى الفني للسهم من الاستوديو:", type=["jpg", "jpeg", "png"], key="chart_uploader")
            
            if uploaded_file is not None:
                image = Image.open(uploaded_file)
                st.image(image, caption="المنحنى المراد تحليله", use_container_width=True)
                
                if st.button("🧐 ابدأ التحليل الفني الشامل", key="analyze_btn"):
                    with st.spinner("جاري فحص الصورة واستخراج الاتجاهات والمؤشرات..."):
                        prompt = (
                            "أنت خبير محترف في التحليل الفني والمالي لأسواق الأسهم (وخاصة البورصة المصرية). "
                            "انظر بعناية إلى لقطة الشاشة المرفقة من تطبيق ثاندر، وقم بما يلي باللغة العربية وبأسلوب مبسط:\n"
                            "1. حدد اتجاه السهم الحالي (صاعد، هابط، عرضي) بناءً على حركة السعر.\n"
                            "2. استخرج نقاط الدعم والمقاومة التقريبية الواضحة في الرسم.\n"
                            "3. انظر إلى مؤشرات حجم التداول (Volume) أو الشموع اليابانية البارزة إن وجدت وعلق عليها.\n"
                            "4. قدم توصية نهائية واضحة ومحددة للمستثمر (شراء / بيع / مراقبة وانتظار) مع ذكر الأسباب الفنية الفورية."
                        )
                        response = client.models.generate_content(model='gemini-2.5-flash', contents=[prompt, image])
                        st.success("🤖 تقرير الفحص الفني:")
                        st.markdown(response.text)
                        
        # --- التبويب الثاني: المستشار المالي النصي ---
        with tab2:
            st.subheader("الاستشارات الاقتصادية والمالية")
            st.write("يمكنك كتابة أي سؤال يدور في ذهنك حول البورصة، الصناديق الاستثمارية، أو استراتيجيات التداول.")
            
            user_question = st.text_area("اكتب سؤالك هنا (مثال: ما رأيك في الاستثمار في أسهم قطاع الأغذية الآن؟ أو كيف أحسب نقطة الخروج من السهم؟):")
            
            if st.button("💬 احصل على النصيحة المالية", key="chat_btn"):
                if user_question:
                    with st.spinner("جاري صياغة النصيحة الاستثمارية الفضلى..."):
                        chat_prompt = (
                            f"أنت مستشار مالي واقتصادي خبير. أجبر على تقديم إجابة احترافية، دقيقة، "
                            f"ومتوازنة باللغة العربية للسؤال التالي، مع إعطاء نصائح تحمي المستثمر من المخاطر: {user_question}"
                        )
                        response = client.models.generate_content(model='gemini-2.5-flash', contents=chat_prompt)
                        st.info("💡 نصيحة المستشار الذكي:")
                        st.markdown(response.text)
                else:
                    st.warning("رجاءً اكتب سؤالك أولاً.")
                    
        # --- التبويب الثالث: أدوات وحاسبات مالية سريعة ---
        with tab3:
            st.subheader("🧮 الحاسبة الاستثمارية السريعة")
            st.write("أداة مساعدة لحساب أرباحك وإدارة مخاطر صفقاتك قبل الدخول فيها.")
            
            buy_price = st.number_input("سعر شراء السهم (بالجنيه):", min_value=0.0, value=10.0, step=0.1)
            quantity = st.number_input("عدد الأسهم المشتراة:", min_value=1, value=100, step=1)
            current_price = st.number_input("سعر السهم الحالي أو سعر البيع المتوقع:", min_value=0.0, value=11.0, step=0.1)
            
            total_cost = buy_price * quantity
            total_value = current_price * quantity
            profit_loss = total_value - total_cost
            percentage = (profit_loss / total_cost) * 100 if total_cost > 0 else 0
            
            st.markdown("---")
            st.write(f"💰 **إجمالي تكلفة الصفقة:** {total_cost:,.2f} جنيه")
            st.write(f"📈 **القيمة الإجمالية الحالية:** {total_value:,.2f} جنيه")
            
            if profit_loss >= 0:
                st.success(f"🟢 **الربح المتوقع:** +{profit_loss:,.2f} جنيه (+{percentage:.2f}%)")
            else:
                st.error(f"🔴 **الخسارة المتوقعة:** {profit_loss:,.2f} جنيه ({percentage:.2f}%)")
                
    except Exception as e:
        st.error(f"حدث خطأ أثناء الاتصال بالذكاء الاصطناعي، تأكد من صحة المفتاح: {e}")
else:
    st.info("⚠️ يرجى إدخال مفتاح Gemini API في الخانة بالأعلى لفتح لوحة التحكم الاحترافية والبدء بالتحليل.")
