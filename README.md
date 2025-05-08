# 🛑 Fake Product Detector — Backend

This is the backend of the Fake Product Detector project — an AI-powered Django system that detects counterfeit products using image classification and review sentiment analysis.

It provides REST APIs for product detection and review analysis.

## 🚀 Features

- 🔍 Detect fake products using an EfficientNetB0 image classification model.
- 💬 Analyze product reviews to detect suspicious or spammy sentiment.
- 🌐 Scrape product reviews from e-commerce sites using Selenium.
- 🔗 Exposes REST APIs for frontend or external apps.

## 🛠️ Tech Stack

- **Framework:** Django, Django REST Framework  
- **Machine Learning:** TensorFlow, Keras, Scikit-learn  
- **Scraping:** Selenium + undetected_chromedriver  
- **Database:** PostgreSQL  
- **Language:** Python 3.10+  

## 📦 Project Structure
```
backend/
├── app/                 # Main app files
│   ├── __init__.py      # App initialization file
│   ├── compare.py       # File for comparing products (if applicable)
│   ├── reviews.py       # Review analysis logic
│   ├── scrapi.py        # Scraping logic
│   ├── sentiment_model.pkl # Pre-trained sentiment analysis model
│   ├── scraper.py       # Scraping logic file
│   ├── tfidf_vectorizer.pkl # TF-IDF model for text processing
│   ├── models.py        # Django models
│   ├── views.py         # Views for handling requests
│   ├── serializer.py    # Serialization for API responses
│   ├── tests.py         # Unit tests
│   └── urls.py          # URL routing for app-specific endpoints
├── product_images/      # Folder to store uploaded product images
│   └── product_images   # (Image files)
├── project/             # Django project configuration
│   ├── __init__.py      # Project's initialization file
│   ├── asgi.py          # ASGI application entry point
│   ├── settings.py      # Django settings file
│   ├── urls.py          # Project-level URL routing
│   └── wsgi.py          # WSGI application entry point
├── .idea/               # IDE-specific configuration (for JetBrains IDEs like PyCharm)
├── .vscode/             # IDE-specific configuration (for Visual Studio Code)
├── db.sqlite3           # SQLite database file (useful in development)
├── manage.py            # Django's management script for running server, migrations, etc.
├── requirements.txt     # Python dependencies for the project
├── venv/                # Virtual environment directory
└── README.md            # Project documentation file

```

## 🧑‍💻 How It Works

**Image Detection API**  
→ Send product image → ML model predicts Real or Fake.

**Review Analysis API**  
→ Send product reviews → Sentiment model analyzes → Flags suspicious products.

Combined detection to enhance accuracy.

## 🔥 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/fake-product-detector-backend.git
cd fake-product-detector-backend
```

### 2. Setup Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations

```bash
python manage.py migrate
```

### 5. Run the Server
```bash
python manage.py runserver
```

### 🎯 API Endpoints
**1. 🔍 Detect Fake Product (Image)**

```curl
POST /api/detect-image/
```
**Request (Form Data)**

| Field | Type | Description        |
| ----- | ---- | ------------------ |
| image | file | Product image file |

**Sample cURL**

```curl
curl -X POST http://localhost:8000/api/detect-image/ \
  -F "image=@/path/to/product.jpg"
```

**Response**

```json
{
  "prediction": "Fake",
  "confidence": 0.87
}
```

### 2. 💬 Analyze Reviews

```curl
POST /api/analyze-reviews/
```

Request (JSON)
```json
{
  "reviews": [
    "This product is terrible, it broke in two days!",
    "Excellent quality, very satisfied!"
  ]
}
```

**Sample cURL**

```curl
curl -X POST http://localhost:8000/api/analyze-reviews/ \
  -H "Content-Type: application/json" \
  -d '{"reviews": ["This product is terrible, it broke in two days!", "Excellent quality, very satisfied!"]}'
```
**Response**

```json
{
  "fake_review_score": 0.65,
  "verdict": "Suspicious"
}
```

## 🏋️ Model Info

	•	Image Detection Model: EfficientNetB0 with transfer learning.
	•	Sentiment Analysis Model: Trained using scikit-learn on product reviews dataset.
	•	Model Storage Location: `ml_models/` directory.

## 🤝 Contributing
Feel free to fork and submit a pull request!

## 📄 License

**MIT License.**



---

### ✅ Now do this:
1. **Copy everything inside that grey box above.**
2. Paste it directly into your `README.md` file.
3. Save → Commit → Push to GitHub.

Result: It will render **perfectly** — no "Copy", no "Edit", and the code blocks will format cleanly.

---

Would you also like me to give you a **bonus tip** on how to preview README formatting locally before pushing to GitHub? (super handy)  
Just say: **"Yes, bonus tip!"**

