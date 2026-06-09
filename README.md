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

## Frontend

A Next.js + TypeScript frontend scaffold has been added in the `./frontend` directory. To run the frontend locally:

```bash
cd frontend
npm install
npm run dev
```

Build for production:

```bash
npm run build
npm start
```

---

## Backend (FastAPI)\n\nA new FastAPI backend was added under `./backend`. To run it locally:\n\n```bash\ncd backend\npython -m pip install -r requirements.txt\nuvicorn app.main:app --reload --host 0.0.0.0 --port 8000\n```\n\nTo build and run with Docker:\n\n```bash\ndocker build -t telegram-export-backend -f backend/Dockerfile backend\ndocker run -p 8000:8000 telegram-export-backend\n```\n\n---

## 🔒 Secrets & Environment Configuration

### Local Development

1. **Create a `.env` file** from the template:
   ```bash
   cp .env.example .env
   ```

2. **Update values** in `.env` with your local development settings:
   ```bash
   DEBUG=True
   ENVIRONMENT=development
   DATABASE_URL=sqlite:///./telegram_export.db
   SECRET_KEY=your-development-secret-key
   ```

3. **Never commit `.env`** — it contains secrets. The `.env.example` file is provided as a reference.

4. **Add `.env` to `.gitignore`** (already configured in this repo).

### Environment Variables Reference

See `.env.example` for all available configuration options:

| Variable | Description | Example |
|----------|-------------|---------|
| `DEBUG` | Enable debug mode (dev only) | `False` |
| `ENVIRONMENT` | deployment environment | `development`, `staging`, `production` |
| `DATABASE_URL` | Database connection string | `sqlite:///./telegram_export.db` |
| `SECRET_KEY` | Application secret key | Generate with `python -c "import secrets; print(secrets.token_urlsafe(32))"` |
| `BACKEND_URL` | Backend API URL | `http://localhost:8000` |
| `FRONTEND_URL` | Frontend URL | `http://localhost:3000` |
| `STRIPE_API_KEY` | Stripe API key (optional) | `sk_test_...` |
| `SENTRY_DSN` | Sentry error tracking (optional) | `https://...@sentry.io/...` |

### GitHub Secrets for CI/CD

Secrets should be stored in GitHub repository settings for use in Actions workflows.

**To add a secret:**

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add secret name and value
4. Click **Add secret**

**Example: Using secrets in GitHub Actions**

```yaml
name: Deploy

on: [push]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          python -m pip install -r requirements.txt
      
      - name: Run with secrets
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
          SECRET_KEY: ${{ secrets.SECRET_KEY }}
          STRIPE_API_KEY: ${{ secrets.STRIPE_API_KEY }}
          SENTRY_DSN: ${{ secrets.SENTRY_DSN }}
        run: |
          python app.py --init-db
          python app.py

      - name: Deploy to production
        env:
          DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
          BACKEND_URL: ${{ secrets.PROD_BACKEND_URL }}
        run: |
          # Your deployment script here
          bash ./scripts/deploy.sh
```

### Recommended Secrets to Configure

**Essential:**
- `SECRET_KEY` — Application secret (generate unique value per environment)
- `DATABASE_URL` — Production database connection

**Optional (if using these services):**
- `STRIPE_API_KEY` — Stripe payments
- `STRIPE_WEBHOOK_SECRET` — Stripe webhooks
- `SENTRY_DSN` — Error tracking
- `OPENAI_API_KEY` — AI features

### Security Best Practices

✅ **DO:**
- Generate strong, unique `SECRET_KEY` for production
- Rotate secrets regularly
- Use environment-specific values (dev ≠ staging ≠ prod)
- Store `.env` in secure location (never share)
- Use GitHub Secrets for CI/CD
- Mask sensitive data in logs

❌ **DON'T:**
- Commit `.env` or `.env.local` files
- Use weak or default secret keys
- Share secrets in chat, email, or code reviews
- Hardcode secrets in code
- Reuse secrets across environments
- Print secrets to stdout/logs

---

✨ **نسخة:** 2.0.0
