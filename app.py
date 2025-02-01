import streamlit as st
from streamlit_option_menu import option_menu
import sqlite3
import os
import tempfile

st.set_page_config(page_title="عبدالله چلاسی - طراح و برنامه نویس",page_icon="logo.png",layout="wide")




with open('c.css') as f:
    st.markdown(f"<style> {f.read()} </style>",unsafe_allow_html=True)





temp_dir = tempfile.gettempdir()

db_path = os.path.join(temp_dir, 'media.db')




# 

# ایجاد پایگاه داده
def create_database():

    

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS media (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video BLOB,
            image BLOB,
            text TEXT
        )
    ''')
    conn.commit()
    conn.close()

# ایجاد جدول نظرات
def create_comments_table():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            comment TEXT NOT NULL,
            approved BOOLEAN NOT NULL DEFAULT 0,
            response TEXT
        )
    ''')
    conn.commit()
    conn.close()

# ذخیره رسانه در پایگاه داده
def save_to_database(video, image, text):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO media (video, image, text) VALUES (?, ?, ?)", (video, image, text))
    conn.commit()
    conn.close()

# دریافت رسانه‌ها از پایگاه داده
def get_media():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM media ORDER BY id DESC")
    data = c.fetchall()
    conn.close()
    return data

# حذف رسانه از پایگاه داده
def delete_media(media_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("DELETE FROM media WHERE id = ?", (media_id,))
    conn.commit()
    conn.close()

# ذخیره نظر کاربر
def save_comment(name, comment):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO comments (name, comment) VALUES (?, ?)", (name, comment))
    conn.commit()
    conn.close()

# دریافت نظرات از پایگاه داده
def get_comments():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM comments ORDER BY id DESC")
    data = c.fetchall()
    conn.close()
    return data

# تأیید نظر کاربر
def approve_comment(comment_id, response):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("UPDATE comments SET approved = 1, response = ? WHERE id = ?", (response, comment_id))
    conn.commit()
    conn.close()

# حذف نظر کاربر
def delete_comment(comment_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
    conn.commit()
    conn.close()

create_database()
create_comments_table()










selected = option_menu (
    menu_title=None,
    options=["تماس با ما","نمونه کار","صفحه اصلی"],
    icons=["envelope","","","house" ],
    menu_icon="cast",
    default_index=2,
    orientation="horizontal",
    styles={
        "container": {"background-color": "#ffffff"},
         "nav-link-selected": {"background-color": "#aca1ef"},
         "nav-link": {"color":"#000000","font-size": "14px", "text-align": "center_y: 0.0", "margin":"0px", "--hover-color": "#afb8fb"},
        
        # "nav-link":{
        #     'font-family': 'Courier New' 'Courier' 'monospace'
        # },
        
    }
)


st.image('logo.png')




if selected == "صفحه اصلی":

    tab1,tab2,tab3=st.tabs(["🏠 خانه","💬 نظرات","🔑 ورود ادمین"])

    with tab1:

    
        with st.container():
            left_column,right_column = st.columns(2)
            with left_column:
    #             st.error("""
    # طراحی سایت با بهترین کیفیت در کمترین زمان    """)
                st.image("https://cdn.dribbble.com/users/1118376/screenshots/3604186/developer-dribbble.gif")

                st.markdown("# :rainbow[ خانه آنلاین کسب و کار شما، وب‌سایت یا اپلیکیشن شماست. با طراحی خلاقانه و کاربرپسند، به راحتی می‌توانید مشتریان جدیدی جذب کنید و خدمات خود را به بهترین شکل ارائه دهید ]")
                st.write("##")


                
            
                st.write("---")
            with right_column:
                # st.divider()
                # st.success("ABDOLLAH CHELASI")
                # st.divider()
                st.write(
                    """
                طراحی وبسایت های :blue[شخصی],:red[خبری],:red[ورزشی],:blue[فروشگاهی] و غیره... مخصوصا برای کسانی که کسب و کار شخصی دارند :red[نصاب],:blue[برق کار و لوله کار],:red[کاشی کار],:blue[نقاش],:red[گچکار] و هر گونه کسب و کار شخصی که دارند.

                :red[طراحی سیستم رزرواسیون هتل]
                و
                :blue[طراحی سیستم نوبت دهی مطب پزشک یا بیمارستان]

                    """
                )
                st.write("##")
                st.write("##")
        

        st.divider()

        

        media = get_media()
        for media_item in media:
            if media_item[1]:  # بررسی وجود ویدیو
                st.video(media_item[1])

                
                  # نمایش ویدیو
            if media_item[2]:
                 # بررسی وجود تصویر
                st.image(media_item[2], use_container_width=True)  # نمایش تصویر
            st.write(media_item[3]) 
            st.error("") 

                

    with tab2:
        st.subheader("نظرات کاربران")
        st.divider()
        name = st.text_input("نام خود را وارد کنید")
        user_comment = st.text_area("نظر خود را بنویسید")
        if st.button("ارسال", key="submit_comment"):
            if name and user_comment:
                save_comment(name, user_comment)
                st.success("نظر شما با موفقیت ارسال شد!")
                st.divider()
            else:
                st.error("لطفا نام و نظر خود را وارد کنید.")

                

        # نمایش نظرات تأیید شده
        comments = get_comments()
        for index, comment in enumerate(comments):
            if comment[3] == 1:  # اگر تأیید شده باشد
                st.divider()
                st.write(f":orange[**{comment[1]} :**] {comment[2]}")  # نام و نظر
                st.write(f" 👨🏻‍💻 :red[**پاسخ ادمین :**] {comment[4]}")  # پاسخ ادمین
                st.divider()






    with tab3:

        admin_password = st.text_input("ورود ادمین", type="password")
        b = st.button("ورود", key="admin_login")

        if admin_password == "abdollah99":
            tab1, tab2 = st.tabs(["فایل", "نظرات"])

            with tab1:
                st.success("خوش آمدید")

                # تب بارگذاری رسانه
                media_type = st.selectbox("Select Media Type", options=["ویدیو", "تصاویر"])
                if media_type == "ویدیو":
                    uploaded_file = st.file_uploader("Upload Video", type=["mp4", "mov", "avi"])
                else:
                    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

                text_input = st.text_area("Enter Description")

                if st.button("Save", key="save_media"):
                    if uploaded_file is not None and text_input:
                        media_data = uploaded_file.read()
                        if media_type == "ویدیو":
                            save_to_database(media_data, None, text_input)  # ذخیره ویدیو
                        else:
                            save_to_database(None, media_data, text_input)  # ذخیره تصویر
                        st.success(f"{media_type} و متن با موفقیت ذخیره شد!")

                    else:
                        st.error("لطفا یک فایل و یک توضیح وارد کنید.")

                # نمایش رسانه‌های بارگذاری شده
                st.subheader("رسانه‌های بارگذاری شده")
                st.divider()
                media = get_media()
                for media_item in media:
                    if media_item[1]:  # بررسی وجود ویدیو
                        st.video(media_item[1])  # نمایش ویدیو
                    if media_item[2]:  # بررسی وجود تصویر
                        st.image(media_item[2], use_container_width=True)  # نمایش تصویر
                    st.write(media_item[3])  # نمایش متن
                    if st.button(f"حذف رسانه {media_item[0]}", key=f"delete_media_{media_item[0]}"):
                        delete_media(media_item[0])
                        st.success(f"رسانه {media_item[0]} با موفقیت حذف شد!")
                        st.rerun()

                    st.warning("") 

            with tab2:
                st.subheader("مدیریت نظرات کاربران")
                st.divider()
                comments = get_comments()
                for comment in comments:
                    st.write(f":green[**{comment[1]} :**] {comment[2]}")  # نام و نظر
    # نام و نظر
                    if comment[3] == 0:  # اگر تأیید نشده است
                        admin_response = st.text_area(f"پاسخ به {comment[1]}", key=f"response_{comment[0]}")
                        
                        if st.button(f"تایید نظر {comment[1]}", key=f"approve_comment_{comment[0]}"):
                            # ارسال نظر به همراه پاسخ (خالی یا پر)
                            approve_comment(comment[0], admin_response if admin_response else "")
                            st.success(f"نظر {comment[1]} تایید شد!")
                            st.rerun()  # رفرش صفحه برای نمایش تغییرات
                            
                    else:
                        st.write(f" 👨🏻‍💻 :red[**پاسخ ادمین :**] {comment[4]}")  # پاسخ ادمین

                    if st.button(f"حذف نظر {comment[1]}", key=f"delete_comment_{comment[0]}"):
                        delete_comment(comment[0])
                        st.success(f"نظر {comment[1]} حذف شد!")
                        st.rerun()  # رفرش صفحه برای نمایش تغییرات

                    st.divider()

        else:
            st.warning("لطفا رمز عبور خود را وارد کنید")







        
elif selected == "نمونه کار":
    with st.container():
        st.success("نمونه کارهای من")
        st.write("##")
        
        # c1 , c2 = st.columns(2)

        # with c1:
    
            
        #     if st.text_input("< CYBER SECURITY >") == "@":
    
        #         st.markdown("[💻 Followers + Instagram 💻](https://followers.streamlit.app/)")



        # st.divider()


        col1 , col2 = st.columns(2)

    with col1:
        with st.expander("هتل ساحل طلایی قشم",expanded=True):
            st.image("h.png")
            st.write("""
هتل ساحل طلایی در 11 کیلومتری قشم است. این هتل قبل‌ها به ساحل سیمین یا پلاژ سیمین معروف بوده. هتل ساحل طلایی از همه نظر هتلی بی‌نظیر در قشم است و طیف گسترده‌ای از خدمات و امکانات را در اختیار مسافران قرار می‌دهد. ساحل اختصاصی هتل بسیار تمیز و خلوت است علاوه بر این‌ها مسافران می‌توانند لذت ماهیگیری را در اسکله‌ی تفریحی هتل تجربه کنند. 
""")
            # st.divider()
            # c1 , c2 = st.columns(2)
            # with c1:
            #     st.markdown("[تحت وب](https://abdollah-hotel.hf.space/)")
            
            # with c2:
            st.markdown("[اپلیکیشن](https://myket.ir/app/com.hotel.abdollahchelasi)")
            st.divider()
            st.markdown("[وبسایت](https://abdollah-hotel.hf.space)")


    with col1:
        with st.expander("موتور قایق مالک",expanded=True):
            st.image("motor.png")
            st.write("""
تعمیرگاه انواع موتورهای دریایی دو زمانه و چهار زمانه و تعمیرات گیربکس و پمپ هیدرولیک جک موتور قایق
""")
            # st.divider()
            # c1 , c2 = st.columns(2)
            # with c1:
            #     st.markdown("[تحت وب](https://abdollah-hotel.hf.space/)")
            
            # with c2:
            st.divider()
            st.markdown("[وبسایت](https://motorqayeq.ir)")



    with col2:
        with st.expander("فروشگاه آموزشی دیجی کد",expanded=True):
            st.image("dig.png")
            st.write("""
آموزش ساخت بازی و برنامه
""")
            # st.divider()
            # c1 , c2 = st.columns(2)
            # with c1:
            #     st.markdown("[تحت وب](https://abdollah-hotel.hf.space/)")
            
            # with c2:
            st.markdown("[اپلیکیشن](https://myket.ir/app/abdollah.digicode)")
            st.divider()
            
            if st.text_input("") == "@":
                st.markdown("[وبسایت](https://abdollah-digicode.hf.space)")

    


    with col2:
        with st.expander("جواهری رز",expanded=True):
            st.image("rozz.png")
            st.write("""
جواهری رز یکی از بهترین جواهر و طلافروشی در جزیره زیبای قشم
""")
            # st.divider()
            # c1 , c2 = st.columns(2)
            # with c1:
            #     st.markdown("[تحت وب](https://abdollah-hotel.hf.space/)")
            
            # with c2:
            st.markdown("[اپلیکیشن](https://myket.ir/app/abdollah.roz)")
            st.divider()
            st.markdown("[وبسایت](https://abdollah-roz.hf.space)")
            st.markdown("[Rose jewelry](https://roz.vercel.app)")
            




    with col2:
        with st.expander("دلفین گربدان",expanded=True):
            st.image("gorb.png")
            st.write("""
باشگاه فوتبال دلفین گربدان یکی از پر افتخارترین و پر هوادارترین باشگاه های فوتبال در جزیره قشم است دلفین گربدان پیش از انقلاب ستاره جنوب گربدان نام داشت باشگاه هم اکنون در لیگ دسته دو قشم قرار گرفته , دلفین گربدان در سال 1324 در جزیره قشم روستای گربدان بنیان گذاری شده است

""")
            # st.divider()
            # c1 , c2 = st.columns(2)
            # with c1:
            #     st.markdown("[تحت وب](https://abdollah-hotel.hf.space/)")
            
            # with c2:
            st.markdown("[اپلیکیشن](https://myket.ir/app/abdollah.gorbedan)")
            st.divider()
            st.markdown("[وبسایت](https://gorbedan.liara.run)")
            st.markdown("[Delfin Gorbadan](https://gorbedan.vercel.app)")
            





    with col1:
        with st.expander("دکوراسیون عبدالباسط",expanded=True):
            st.image("dekorb.png")
            st.write("""
خدمات دکوراسیون خانه < نصب PVC , نصب کناف , نصب ترمووال , نصب قرنیز و نصب ماربل شیت > با طرح های مختلف در سر تا سر جزیره قشم انجام میشود >

""")
            # st.divider()
            # c1 , c2 = st.columns(2)
            # with c1:
            #     st.markdown("[تحت وب](https://abdollah-hotel.hf.space/)")
            
            # with c2:
            st.markdown("[اپلیکیشن](https://myket.ir/app/abdollah.dekor)")
            st.divider()
            st.markdown("[وبسایت](https://abdollah-dekor.hf.space)")
            






        col1,col2=st.columns((2))

        
        with col1:
            with st.expander(" فروشگاه دیجی کد " ,expanded=True):
                st.image("dig.png")
                st.write("""
                         فروشگاه آموزشی دیجی کد با کلی سورس های آماده و اینکه بتونم با کدهای کمتری یک برنامه کامل بسازم و اینکه سعی میکنم کسانی که برنامه نویسی بلد نیستن و علاقه دارن همچین پروژه هایی بسازن و نمیخوان خیلی درگیر برنامه نویسی باشن پروژه هایی که با علامت ✨ روی پروژه ها برچسب زده شده رو اینجور پروژه ها برنامه های کامل زده شده و کد کمتری دارن
                         """)
                # st.markdown("[دیجی کد](https://digicode.streamlit.app/)")
        
        with col2:

            with st.expander("وب سایت خدمات پی وی سی - رمکان",expanded=True):
                st.image("pvc.png")
                st.write("""
    اجرای نصب پی وی سی در سراسر جزیره قشم        """)
                # st.markdown("[Pvc-Ramkan](http://pvcahmad.ir)")
            

        
        with col1:

            with st.expander("VeTube",expanded=True):
                st.image("hotel.png")
                st.write("""
            VeTube - Garden City Hotel Dubai
""")
                st.markdown("[VeTube - Dubai](http://vetube.streamlit.app)")
            
    


        with col2:
                with st.expander("دکوراسیـون شادمان - رمکان" ,expanded=True):
                    st.image("upvc.png")
                    st.write("""
    تولیدی درب و پنجره یو پی وی سی نوین ترک , فروش و نصب پی وی سی , طراحی یا ساخت و اجرای انواع سایبان پی وی سی        """)
                    st.markdown("[Dekorasion Shademan](https://pvcshademan.streamlit.app)")
        
        
        


        with col1:
            
                

            with st.expander("دکوراسیون لنج محمد" ,expanded=True):
                st.image("dekor.png")
                st.write("""
                             خدمات دکوراسیون لنج
                             """)
                # col1,col2=st.columns([2,3])
                # with col1:
                #     st.markdown("[DekorLenj](https://dekorlenj.ir/)")
                        
                # with col2:
                        
                st.markdown("[LenjDekor](https://lenjdekor.streamlit.app/)")
                        
                       
                       

        col1,col2=st.columns((2))

        with col1:
            with st.expander("خدمات اینترنتی طالب" ,expanded=True):
                st.image("taleb.png")
                st.write("""
    خدمات نمایندگی طالب با نصب اولیه وای فای رایگان و شارژ اینترنتی اینترنتی و فروش تجهیزات وای فای با قیمت های مختلف در سراسر جزیره قشم    """)
                # st.markdown("[Taleb internet services](https://taleb.vercel.app/)")
        

        with col2:
            with st.expander("عمر الزبير المرزوقي" ,expanded=True):
                st.image("omar.png")
                st.write("""
    اول حكم يكسر قاعدة احتكار حكام أوربا على نهائيات كاس العالم لكرة اليد """)
                st.markdown("[عمر الزبير المرزوقي](https://omarzubair.vercel.app/)")
        
            with col2:
                with st.expander("Mazaya Car Rental, Dubai" ,expanded=True):
                    st.image("mazaya.png")
                    st.write("""
    🇦🇪 اجاره ماشین مازایا، دبی 🇦🇪    """)
                    st.markdown("[Mazaya Car Rental Dubai](https://mazaya-cars.vercel.app/)")
        
            
            
            
                       
                        
            with col1:

                with st.expander("دکوراسیون شادمان" ,expanded=True):
                    
                    st.image("sh.png")
                    st.write("""
                             دکوراسیون شادمان
                             """)
                    
                    # st.markdown("[shademan](https://pvcshademan.streamlit.app/)")
                        
                    
            with col2:

                with st.expander("نقاش علی اکبر بندرعباس" ,expanded=True):
                    
                    st.image("naqash.png")
                    st.write("""
                             خدمات نقاشی علی اکبر در سر تا سر بندرعباس
                             """)
                    
                    # st.markdown("[aliakbar](https://aliakbar.streamlit.app/)")
                                
                    
        

            with col1:

                with st.expander("خبر3" ,expanded=True):
                    
                    st.image("kh.png")
                    st.write("""
                             آخرین خبرهای ورزشی رو دنبال کنید
                             """)
                    
                    # st.markdown("[Khabar3](https://khabar3.onrender.com/)")
                        
                    








if selected == "تماس با ما":
    

    with st.container():

        

        
        
       


        imgabdollah , abdollah = st.columns(2)

        with imgabdollah:

            st.image("a.jpg",width=200)
            st.warning("📞 00989335825325 📞")

        with abdollah:

            st.error("عبداالله چلاسی")

            st.write("""
    من متولد 1373 قشم - روستای گربدان هستم که در زمینه طراحی وب , دسکتاپ و برنامه نویسی موبایل فعالیت دارم و به صورت آزاد یا همون فریلنسینگ کار میکنم, یکی از اتفاقات جالب زندگیم اینه که تفریحم و شغلم یکی هستند و اونم چیزی نیست جز توسعه وب و اپلیکیشن , این داستان از سال 1391 شروع شد که به سمت تکنولوژی و دنیای برنامه نویسی پا گذاشتم همچنان این سابقه با گذر زمان همچنان بیشتر و بیشتر میشه، چون برنامه نویسی چیزی هست که من باهاش دنیا رو می بینم، می سنجم و حس میکنم،و سعی ام بر این است که با همین روند پیش برم و روز به روز با تکنولوژی های جدید دنیای برنامه نویسی کار کنم و تجربیات جدیدی کسب کنم         """)

            

            st.video('a.mp4')



# -------CONTACT-------

    with st.container():
        
        st.write("---")
        st.write("##")

        st.success("برای سفارش پروژه تماس یا پیام ارسال کنید")

        col1,col2=st.columns(2)
        with col1:
            
            st.markdown("[📞 تماس](tel:00989335825325)")
            
        with col2:
            
            st.markdown("[💬 ارسال پیام](sms:00989335825325)")

        
            
            
            


st.divider()

st.markdown("[عبدالله چلاسی](https://abdollahchelasi.ir)")
