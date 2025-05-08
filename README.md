🛑 Fake Product Detector — Backend
This is the backend of the Fake Product Detector project — an AI-powered Django system that detects counterfeit products using image classification and review sentiment analysis.

It provides REST APIs for product detection and review analysis.

🚀 Features
🔍 Detect fake products using an EfficientNetB0 image classification model.

💬 Analyze product reviews to detect suspicious or spammy sentiment.

🌐 Scrape product reviews from e-commerce sites using Selenium.

🔗 Exposes REST APIs for frontend or external apps.

🛠️ Tech Stack
Framework: Django, Django REST Framework

Machine Learning: TensorFlow, Keras, Scikit-learn

Scraping: Selenium + undetected_chromedriver

Database: PostgreSQL

Language: Python 3.10+

📦 Project Structure
bash
Copy
Edit
backend/
├── project/          # Django project files
├── apps/
│   ├── products/     # Product detection app (image-based)
│   ├── reviews/      # Review analysis app
├── ml_models/
│   ├── fake_product_detector.h5
│   ├── sentiment_model.pkl
├── scraping/
│   ├── scraper.py    # Selenium scraper
├── requirements.txt
└── README.md
🧑‍💻 How It Works
Image Detection API
→ Send product image → ML model predicts Real or Fake.

Review Analysis API
→ Send product reviews → Sentiment model analyzes → Flags suspicious products.

Combined detection to enhance accuracy.

🔥 Getting Started
1. Clone the Repo
bash
Copy
Edit
git clone https://github.com/your-username/fake-product-detector-backend.git
cd fake-product-detector-backend
2. Setup Virtual Environment
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Apply Migrations
bash
Copy
Edit
python manage.py migrate
5. Run the Server
bash
Copy
Edit
python manage.py runserver
🎯 API Endpoints
1. 🔍 Detect Fake Product (Image)
POST /api/detect-image/

Request (Form Data)
Field	Type	Description
image	file	Product image file

Sample cURL
bash
Copy
Edit
curl -X POST http://localhost:8000/api/detect-image/ \
  -F "image=@/path/to/product.jpg"
Response
json
Copy
Edit
{
  "prediction": "Fake",
  "confidence": 0.87
}
2. 💬 Analyze Reviews
POST /api/analyze-reviews/

Request (JSON)
json
Copy
Edit
{
  "reviews": [
    "This product is terrible, it broke in two days!",
    "Excellent quality, very satisfied!"
  ]
}
Sample cURL
bash
Copy
Edit
curl -X POST http://localhost:8000/api/analyze-reviews/ \
  -H "Content-Type: application/json" \
  -d '{"reviews": ["This product is terrible, it broke in two days!", "Excellent quality, very satisfied!"]}'
Response
json
Copy
Edit
{
  "fake_review_score": 0.65,
  "verdict": "Suspicious"
}
🏋️ Model Info
Image Detection: EfficientNetB0 + transfer learning

Sentiment Analysis: Trained using scikit-learn on product reviews dataset

Pre-trained models stored in ml_models/ directory.

🤝 Contributing
Feel free to fork and submit a pull request!

📄 License
MIT License.
