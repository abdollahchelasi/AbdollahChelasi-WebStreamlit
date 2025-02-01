FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install system dependencies (without Node.js and npm)
RUN apt-get update -y && \
    apt-get install -y libgl1-mesa-glx libglib2.0-0

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the entire application code
COPY . .

# Streamlit configuration
RUN mkdir -p /root/.streamlit
RUN bash -c 'echo -e "\
[general]\n\
email = \"\"\n\
" > /root/.streamlit/credentials.toml'
RUN bash -c 'echo -e "\
[server]\n\
enableCORS = false\n\
" > /root/.streamlit/config.toml'

# Replace the existing title and noscript tags and inject the new meta tags
RUN sed -i "s|<noscript>.*</noscript>|<noscript>طراحی وبسایت‌های شخصی، خبری، ورزشی، فروشگاهی و غیره... مخصوصا برای کسانی که کسب و کار شخصی دارند (نصاب، برق کار، لوله کار، کاشی کار، نقاش، گچ کار و هر گونه کسب و کار شخصی). طراحی سیستم رزرواسیون هتل و طراحی سیستم نوبت دهی مطب پزشک یا بیمارستان.</noscript>|g" /usr/local/lib/python3.11/site-packages/streamlit/static/index.html && \
    sed -i '/<head>/,/<\/head>/s|<\/head>|\
    <meta charset="UTF-8">\n\
    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n\
    <link rel="icon" href="https://abdollahchelasi.ir/media/0ad2abce143d4937ae0e0fd8d88632394d6c622bd7b2df49de7ec8f9.png">\n\
    <!-- Primary Meta Tags -->\n\
    <title>عبدالله چلاسی - طراح و برنامه نویس وبسایت</title>\n\
    <meta name="description" content="طراحی وبسایت‌های شخصی، خبری، ورزشی، فروشگاهی و غیره... مخصوصا برای کسانی که کسب و کار شخصی دارند (نصاب، برق کار، لوله کار، کاشی کار، نقاش، گچ کار و هر گونه کسب و کار شخصی). طراحی سیستم رزرواسیون هتل و طراحی سیستم نوبت دهی مطب پزشک یا بیمارستان." />\n\
    <meta name="keywords" content="عبدالله چلاسی, طراحی سایت قشم, طراحی سایت رزرواسیون هتل قشم, طراحی سیستم نوبت دهی مطب, طراحی سایت با کمترین هزینه" />\n\
    <meta name="author" content="عبدالله چلاسی" />\n\
    <meta name="image" content="https://abdollahchelasi.ir/media/0ad2abce143d4937ae0e0fd8d88632394d6c622bd7b2df49de7ec8f9.png" />\n\
    <meta name="robots" content="index, follow">\n\
    <link rel="canonical" href="https://abdollahchelasi.ir" />\n\
    <meta property="og:type" content="website" />\n\
    <meta property="og:url" content="https://abdollahchelasi.ir" />\n\
    <meta property="og:site_name" content="عبدالله چلاسی">\n\
    <meta property="og:title" content="عبدالله چلاسی - طراح و برنامه نویس وبسایت" />\n\
    <meta property="og:description" content="طراحی وبسایت‌های شخصی، خبری، ورزشی، فروشگاهی و غیره... مخصوصا برای کسانی که کسب و کار شخصی دارند (نصاب، برق کار، لوله کار، کاشی کار، نقاش، گچ کار و هر گونه کسب و کار شخصی). طراحی سیستم رزرواسیون هتل و طراحی سیستم نوبت دهی مطب پزشک یا بیمارستان." />\n\
    <meta property="og:image" content="https://abdollahchelasi.ir/media/0ad2abce143d4937ae0e0fd8d88632394d6c622bd7b2df49de7ec8f9.png" />\n\
    <meta property="og:locale" content="fa_IR" />\n\
    <meta name="twitter:card" content="summary_large_image">\n\
    <meta name="twitter:image" content="https://abdollahchelasi.ir/media/0ad2abce143d4937ae0e0fd8d88632394d6c622bd7b2df49de7ec8f9.png">\n\
    <script type="application/ld+json">\n\
    {\n\
        "@context": "https://schema.org",\n\
        "@type": "WebSite",\n\
        "name": "عبدالله چلاسی - طراح و برنامه نویس وبسایت",\n\
        "url": "https://abdollahchelasi.ir",\n\
        "description": "طراحی وبسایت‌های شخصی، خبری، ورزشی، فروشگاهی و غیره... مخصوصا برای کسانی که کسب و کار شخصی دارند (نصاب، برق کار، لوله کار، کاشی کار، نقاش، گچ کار و هر گونه کسب و کار شخصی). طراحی سیستم رزرواسیون هتل و طراحی سیستم نوبت دهی مطب پزشک یا بیمارستان.",\n\
        "image": "https://abdollahchelasi.ir/media/0ad2abce143d4937ae0e0fd8d88632394d6c622bd7b2df49de7ec8f9.png"\n\
    }\n\
    </script>\n\
    <script type="application/ld+json">\n\
    {\n\
        "@context": "https://schema.org",\n\
        "@type": "Organization",\n\
        "name": "عبدالله چلاسی - طراح و برنامه نویس وبسایت",\n\
        "url": "https://abdollahchelasi.ir",\n\
        "logo": "https://abdollahchelasi.ir/media/0ad2abce143d4937ae0e0fd8d88632394d6c622bd7b2df49de7ec8f9.png",\n\
        "description": "طراحی وبسایت‌های شخصی، خبری، ورزشی، فروشگاهی و غیره... مخصوصا برای کسانی که کسب و کار شخصی دارند (نصاب، برق کار، لوله کار، کاشی کار، نقاش، گچ کار و هر گونه کسب و کار شخصی). طراحی سیستم رزرواسیون هتل و طراحی سیستم نوبت دهی مطب پزشک یا بیمارستان.",\n\
        "address": {\n\
            "@type": "PostalAddress",\n\
            "addressLocality": "گربدان",\n\
            "addressRegion": "قشم",\n\
            "addressCountry": "IR"\n\
        },\n\
        "contactPoint": {\n\
            "@type": "ContactPoint",\n\
            "telephone": "+989335825325",\n\
            "contactType": "customer service"\n\
        }\n\
    }\n\
    </script>\n\
    </head>|' /usr/local/lib/python3.11/site-packages/streamlit/static/index.html

EXPOSE 8501

# Run Streamlit app
CMD ["streamlit", "run", "app.py"]
