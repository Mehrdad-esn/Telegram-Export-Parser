# 🚀 Advanced Telegram Export Parser

تبدیل صادرات تلگرام (JSON) به فرمت‌های مختلف با قابلیت تحلیل و فیلترینگ پیشرفته

## ✨ ویژگی‌های جدید

### 📊 آمار و تحلیل (Statistics)

- تعداد کل پیام‌ها
- شمار پیام‌ها برای هر کاربر
- میانگین طول پیام
- کلمات پر استفاده
- تحلیل روزانه
- بهترین سخنران‌ها

### 🎯 فیلترهای پیشرفته

- فیلتر بر اساس بازه تاریخی
- جستجو براساس نام کاربر
- جستجو براساس کلمات کلیدی
- پشتیبانی Regex
- فیلتر براساس طول پیام
- فیلتر براساس وسایط (رسانه)

### 📁 فرمت‌های صادراتی

- **TXT** - متن ساده (پیش‌فرض)
- **CSV** - برای Excel/Sheets
- **JSON** - فرمت ساختاریافته
- **HTML** - نمایش وب
- **Markdown** - برای اسناد
- **Excel** - فایل XLSX

### 📈 نمودار و تقریر

- خلاصه آماری خودکار
- تقریر توزیع سخنران‌ها
- تجزیه‌و‌تحلیل کلمات

## 📦 نصب

```bash
# نصب بسته‌های مورد نیاز
pip install -r requirements.txt
```

**بسته‌های اختیاری:**

- `ijson` - پردازش فایل‌های بزرگ
- `tqdm` - نشان‌دهنده پیشرفت
- `openpyxl` - صادرات Excel

## 🎮 استفاده

### حالت تعاملی (پیش‌فرض)

```bash
python app.py -i result.json
```

### صادرات چت خاص

```bash
python app.py -i result.json -c "نام چت"
```

### صادرات تمام چت‌ها

```bash
python app.py -i result.json --all-chats
```

### صادرات به فرمت‌های مختلف

```bash
# CSV
python app.py -i result.json --format csv

# Excel
python app.py -i result.json --format xlsx

# HTML
python app.py -i result.json --format html

# Markdown
python app.py -i result.json --format md
```

### نمایش آمار

```bash
# با صادرات
python app.py -i result.json --stats

# تنها آمار (بدون صادرات)
python app.py -i result.json --stats-only
```

### تغییر دایرکتوری خروجی

```bash
python app.py -i result.json -o ./my_exports
```

## 📚 مثال‌های عملی

### صادرات چند چت به Excel

```bash
python app.py -i data.json --all-chats --format xlsx
```

### صادرات و مشاهده آمار

```bash
python app.py -i data.json -c "دوستان" --format html --stats
```

## 🏗️ ساختار پروژه

```
Telegram Export Parser/
├── app.py              # برنامه اصلی
├── utils.py            # توابع کمکی
├── stats.py            # ماژول آمار
├── filters.py          # ماژول فیلترها (آینده)
├── exporters.py        # ماژول صادرات چند‌فرمت
├── requirements.txt    # بسته‌های مورد نیاز
└── README.md          # این فایل
```

## 🔄 فرمت‌ های خروجی

### CSV

```
id,timestamp,sender,text,reply_to_id
1,2024-01-15 10:30,علی,سلام دنیا,
2,2024-01-15 10:31,محمد,علیک assalam,1
```

### Excel

جدول قابل ویرایش با رنگ‌آمیزی هدر

### HTML

صفحه وب تک‌صفحه‌ای قابل نمایش در مرورگر

### Markdown

فایل متن برای مستندات

## 🎯 برنامه آینده

- [ ] فیلترهای پیشرفته (تاریخ، کاربر، کلمات)
- [ ] ترجمه خودکار پیام‌ها
- [ ] تحلیل احساسات
- [ ] رابط کاربری وب (Web UI)
- [ ] پشتیبانی از داده‌بازهای محلی
- [ ] نمودار و گراف‌های تعاملی

## ⚙️ پیکربندی

### متغیرهای محیط

```bash
export TELEGRAM_PARSER_OUTPUT=/custom/output/dir
python app.py -i result.json
```

## 🐛 عیب‌یابی

### خطای "ijson not installed"

```bash
pip install ijson
```

### فایل خروجی بزرگ

برنامه خودکار به حالت streaming نمیرود. برای فایل‌های بزرگ (>100MB) از `ijson` استفاده کنید.

## 📝 لایسنس

MIT License

## 👨‍💻 مشارکت

برای بهبود پروژه:

1. Fork کنید
2. Branch جدید بسازید
3. تغییرات خود را commit کنید
4. PR بفرستید

## ❓ سوالات متداول

**Q: آیا می‌توانم داده‌های خصوصی خود را محافظت کنم؟**
A: بله، تمام پردازش محلی انجام می‌شود.

**Q: آیا برای فایل‌های بزرگ (1GB+) کار می‌کند؟**
A: بله، با استفاده از ijson برای streaming.

**Q: آیا می‌توانم خود exporters را بسازم؟**
A: بله، از کلاس BaseExporter در exporters.py ارث‌بری کنید.

---

✨ **نسخه:** 2.0.0
