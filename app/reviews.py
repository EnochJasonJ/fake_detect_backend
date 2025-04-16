import os
# from datetime import datetime
import django
import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE","project.settings")
django.setup()
import joblib
import numpy as np
from colorama import Fore, Style
ai = joblib.load('app/sentiment_model.pkl')
from app.models import StoreURLDetailsModel
product = StoreURLDetailsModel.objects.all()

def predictReview(review_text):
    try:
        prediction = ai.predict([review_text])[0]
        print(prediction)
        return prediction
            
    except Exception as e:
        print(f"Error processing reviews for: {e}")
        print(str(e))