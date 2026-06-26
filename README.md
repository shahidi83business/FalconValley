# FalconValley — راهنمای استقرار

## پیش‌نیازها

- Python 3.10+
- MongoDB (نصب محلی یا MongoDB Atlas)
- Bot Token از BotFather
- OpenAI API Key

---

## نصب سریع

```bash
git clone <your-repo-url>
cd FalconValley
bash setup.sh
#!/bin/bash
# set -e

# echo "🚀 FalconValley Setup"
# echo "====================="

# # ساخت virtual environment
# if [ ! -d "venv" ]; then
#     echo "📦 Creating virtual environment..."
#     python3 -m venv venv
# fi

# # فعال‌سازی venv
# source venv/bin/activate

# # نصب پکیج‌ها
# echo "📥 Installing dependencies..."
# pip install --upgrade pip -q
# pip install -r requirements.txt -q

# # ساخت .env از روی .env.example
# if [ ! -f ".env" ]; then
#     echo "⚙️  Creating .env from .env.example..."
#     cp .env.example .env
#     echo "✏️  Please edit .env and fill in your values, then run:"
#     echo "    source venv/bin/activate && python run.py"
# else
#     echo "✅ .env already exists"
#     echo ""
#     echo "▶️  To start the bot:"
#     echo "    source venv/bin/activate && python run.py"
# fi

# echo ""
# echo "✅ Setup complete!"
# ```

سپس فایل `.env` را باز کنید و مقادیر واقعی را وارد کنید:

```bash
nano .env
```

---

## اجرا

```bash
source venv/bin/activate
python run.py
```

---

## متغیرهای محیطی (.env)

| متغیر | توضیح | مثال |
|---|---|---|
| `BOT_TOKEN` | توکن ربات تلگرام | `123456:ABC...` |
| `BASE_URL` | آدرس پایه API تلگرام | `https://api.telegram.org/bot` |
| `MONGO_URI` | آدرس اتصال MongoDB | `mongodb://localhost:27017` |
| `DB_NAME` | نام دیتابیس | `ecokirom` |
| `OPENAI_API_KEY` | کلید API اوپن‌ای | `sk-...` |
| `OPENAI_BASE_URL` | آدرس پایه OpenAI | `https://api.openai.com/v1` |

---

## رفع خطاها

### خطا: `ConnectionFailure` (MongoDB)
```
❌ Failed to connect to MongoDB
```
راه‌حل: مطمئن شوید MongoDB در حال اجرا است:
```bash
sudo systemctl start mongod
```

### خطا: `BOT_TOKEN` خالی است
```
AttributeError: 'NoneType' + ...
```
راه‌حل: فایل `.env` را بررسی کنید و مطمئن شوید `BOT_TOKEN` مقدار دارد.

### خطا: `ModuleNotFoundError`
```bash
pip install -r requirements.txt
```

---

## آپدیت پروژه

```bash
git pull
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

---

## ساختار پروژه

```
FalconValley/
├── app/
│   ├── ai/          # RAG و هوش مصنوعی
│   ├── bot/         # Telegram API
│   ├── data/        # دیتابیس و مدل‌ها
│   ├── game/        # منطق بازی
│   ├── services/    # سرویس‌های کمکی
│   └── main.py      # نقطه ورود اصلی
├── .env.example     # نمونه متغیرهای محیطی
├── requirements.txt
├── run.py           # اجرای پروژه
└── setup.sh         # راه‌اندازی خودکار
```
