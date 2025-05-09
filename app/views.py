from django.shortcuts import render, get_object_or_404
import requests
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from .models import GetUrlModel, StoreURLDetailsModel
from .serializer import URLSerializers, LoginSerializer, UserSerializer, ScrapeURLSerializer
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import  ContentType
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from rest_framework.generics import ListCreateAPIView, DestroyAPIView, GenericAPIView , CreateAPIView
from rest_framework.views import APIView
# from app.scrape import scrapeAmazon
from app.scrapi import scrape, scrape_flipkart, scrape_myntra, scrape_reliance, scrape_snapdeal
# from app.scrapeSelenium import scrapeAmazonSelenium
from django.core.files.base import ContentFile
import joblib
from urllib.parse import urlparse
lr_model = joblib.load('app/sentiment_model.pkl')
from app.reviews import predictReview

ecommerce_domains = [
    "www.amazon.com",
    "www.flipkart.com","www.snapdeal.com", "www.myntra.com", "www.reliancedigital.in","www.instagram.com"
]

class CurrentUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = request.user
        return Response({"username": user.username})

domain_set = set(ecommerce_domains)

def validate_site(url):
    return any(domain in url for domain in domain_set)
    domain = urlparse(url).netloc
    return domain in domain_set



def hello(request):
    return HttpResponse("HEllo")

class Register(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save()



class postURL(ListCreateAPIView):
    serializer_class = URLSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GetUrlModel.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DeleteURL(DestroyAPIView):
    queryset = StoreURLDetailsModel.objects.all()
    serializer_class = URLSerializers
    lookup_field = 'pk'

class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self,request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token,created = Token.objects.get_or_create(user=user)
        return Response({
            "message": "Logged in",
            "username": user.username,
            "token": token.key,
        },status=HTTP_200_OK)
    
def scrape_by_url(url):
    if "amazon." in url:
        return scrape(url)
    elif "flipkart." in url:
        return scrape_flipkart(url)
    elif "myntra." in url:
        return scrape_myntra(url)
    elif "reliancedigital." in url or "reliance." in url:
        return scrape_reliance(url)
    elif "snapdeal." in url:
        return scrape_snapdeal(url)
    else:
        return {"error": "Unsupported e-commerce site!"}

class ScrapeURLView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ScrapeURLSerializer

    def get_queryset(self):
        return StoreURLDetailsModel.objects.filter(user=self.request.user)

    def post(self, request):
        product_url = request.data.get('Product_URL')

        if not product_url:
            return Response({"error": "Product URL is Required!"}, status=HTTP_400_BAD_REQUEST)

        if not validate_site(product_url):  # Ensure this is working as expected
            return Response({"error": "Invalid URL: Not an E-Commerce site!"}, status=HTTP_400_BAD_REQUEST)
#not scraped_data or 
        try:
            scraped_data = scrape_by_url(product_url)
            if not scraped_data or "error" in scraped_data:
                return Response({"error": scraped_data.get("error", "Couldn't fetch product data!")}, status=HTTP_200_OK)
            reviews = scraped_data.get('reviews',[])
            sentimen_reviews=[]
            positive_rev=0
            neg_rev=0
            answer = ""
            review_count = scraped_data.get('review_count', 0)
            # print(reviews[0])
            for p in reviews:
                try:
                    review_text = str(p).strip()
                    prediction = predictReview(review_text)
                    sentimen_reviews.append(prediction)
                    if prediction == "Positive":
                        positive_rev += 1
                    elif prediction == "Negative":
                        neg_rev += 1
                except Exception as e:
                    print(f"Error:{e}")
            total_reviews = len(reviews)
            # if total_reviews <= 3:
            #     answer = "Suspicious Product"
            if positive_rev > neg_rev:
                answer = "Genuine Product"
            else:
                answer = "Suspicious Product"
            product = StoreURLDetailsModel.objects.create(
                user=request.user,
                title=scraped_data.get("title", ""),
                Product_URL=product_url,
                description=scraped_data.get("description", ""),
                reviews=reviews,
                sentiment = answer,
                review_count=review_count,
                ratings_count=scraped_data.get("ratings_count", 0),
            )
            image_url = scraped_data.get("image", "")
            if image_url and image_url.startswith("http"):
                try:
                    img_resp = requests.get(image_url, stream=True)
                    img_resp.raise_for_status() 
                    image_content = ContentFile(img_resp.content)
                    product.image.save("Product.jpg", image_content)
                except requests.exceptions.RequestException as e:
                    print(f"Error downloading image: {e}")

            return Response({
                "message": "Product scraped and saved successfully!",
                "title": scraped_data.get("title", ""),
                "Product_URL": product_url,
                "description": scraped_data.get("description", ""),
                "image": image_url,
                "reviews": reviews,
                "sentiment": answer,
                "review_count": review_count,
            }, status=HTTP_201_CREATED)

        except Exception as err:
            print(f"Error: {err}")
            return Response({"error": str(err)}, status=HTTP_400_BAD_REQUEST)

class ProductDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        product = get_object_or_404(StoreURLDetailsModel, pk=pk, user=request.user)
        return Response({
            "title": product.title,
            "Product_URL": product.Product_URL,
            "description": product.description,
            "image": product.image.url if product.image else None,
            "reviews": product.reviews,
            "sentiment": product.sentiment,
            "review_count": product.review_count,
            "ratings_count": product.ratings_count,
        }, status=HTTP_200_OK)