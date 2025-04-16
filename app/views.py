from django.shortcuts import render
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
    "www.amazon.com", "www.ebay.com", "www.aliexpress.com", "www.walmart.com", "www.etsy.com",
    "www.flipkart.com", "www.bestbuy.com", "www.shopify.com", "www.target.com", "www.newegg.com",
    "www.rakuten.com", "www.overstock.com", "www.jd.com", "www.zappos.com", "www.wayfair.com",
    "www.bonanza.com", "www.lazada.com", "www.cdiscount.com", "www.wish.com", "www.costco.com",
    "www.samsclub.com", "www.bhphotovideo.com", "www.sephora.com", "www.adoreme.com", "www.macy's.com",
    "www.kohls.com", "www.shein.com", "www.forever21.com", "www.asos.com", "www.alibaba.com",
    "www.dell.com", "www.pcworld.com", "www.bunnings.com.au", "www.bunningswarehouse.com.au",
    "www.target.com.au", "www.bigw.com.au", "www.catch.com.au", "www.myer.com.au", "www.sainsburys.co.uk",
    "www.argos.co.uk", "www.currys.co.uk", "www.johnlewis.com", "www.marksandspencer.com", "www.harrods.com",
    "www.ao.com", "www.carrefour.com", "www.lidl.com", "www.woolworths.com.au", "www.zara.com", "www.hm.com",
    "www.uniqlo.com", "www.jcpenney.com", "www.shopbop.com", "www.modcloth.com", "www.bonprix.com",
    "www.zalando.com", "www.otto.de", "www.notonthehighstreet.com", "www.farfetch.com", "www.bq.com",
    "www.ldlc.com", "www.mediamarkt.com", "www.allegro.pl", "www.empik.com", "www.dm.de", "www.dm-drogeriemarkt.de",
    "www.rakuten.co.jp", "www.mercadolibre.com", "www.submarino.com.br", "www.magazineluiza.com.br",
    "www.carrefour.com.br", "www.loja.vivareal.com.br", "www.b2w.com.br", "www.extra.com.br", "www.shopclues.com",
    "www.paytm.com", "www.flipkart.com", "www.snapdeal.com", "www.myntra.com", "www.pepperfry.com", "www.tatacliq.com",
    "www.bigbasket.com", "www.grofers.com", "www.nykaa.com", "www.tata.com", "www.croma.com", "www.limeroad.com",
    "www.shopify.in", "www.shoppersstop.com", "www.lenskart.com", "www.nytimes.com", "www.zoomcar.com", "www.quikr.com",
    "www.olx.in", "www.makemytrip.com", "www.cleartrip.com", "www.redbus.in", "www.justdial.com", "www.bookmyshow.com",
    "www.irctc.co.in", "www.wayfair.ca", "www.sephora.ca", "www.canadiantire.ca", "www.costco.ca", "www.walmart.ca",
    "www.hudsonsbay.com", "www.saksfifthavenue.com", "www.shop.ca", "www.indigo.ca", "www.homehardware.ca",
    "www.bunnings.com.au", "www.woolworths.com.au", "www.petbarn.com.au", "www.sephora.com.au", "www.kmart.com.au",
    "www.harveynorman.com.au", "www.freedom.com.au", "www.theiconic.com.au", "www.bigw.com.au", "www.kmart.co.nz",
    "www.nzherald.co.nz", "www.trademe.co.nz", "www.briscoes.co.nz", "www.smithscity.co.nz", "www.thewarehouse.co.nz",
    "www.shoprite.com", "www.pylones.com", "www.bluedog.com", "www.bluefly.com", "www.home24.com", "www.mango.com",
    "www.dunelm.com", "www.lancome-usa.com", "www.sunglasshut.com", "www.warbyparker.com", "www.toms.com",
    "www.wholesalehunter.com", "www.fossil.com", "www.ugg.com", "www.swatch.com", "www.fragrancex.com", "www.perfume.com",
    "www.bose.com", "www.sonos.com", "www.vizio.com", "www.crestron.com", "www.harman.com", "www.lenovo.com",
    "www.compuplus.com", "www.bose.com", "www.bose.co.uk", "www.sennheiser.com", "www.plantronics.com",
    "www.bluejeans.com", "www.poly.com", "www.headphones.com", "www.headphonestreat.com", "www.skullcandy.com",
    "www.uggaustralia.com", "www.northface.com", "www.columbia.com", "www.patagonia.com", "www.rei.com", "www.johnlewis.com",
    "www.thehut.com", "www.lookfantastic.com", "www.feelunique.com", "www.beautybay.com", "www.cultbeauty.com",
    "www.hairtrade.com", "www.lookfantastic.com", "www.sephora.com", "www.boots.com", "www.drugstore.com",
    "www.superdrug.com", "www.sainsburys.co.uk", "www.asda.com", "www.tesco.com", "www.primark.com", "www.matalan.co.uk",
    "www.thebodyshop.com", "www.fiftyfifty.co.uk", "www.cowshed.com", "www.elizabetharden.co.uk", "www.t3.com",
    "www.ebay.co.uk", "www.groupon.co.uk", "www.onbuy.com", "www.bigbasket.com", "www.flipkart.com", "www.pepperfry.com",
    "www.snapdeal.com", "www.myntra.com", "www.instamojo.com", "www.fluentcommerce.com", "www.grocerygateway.com",
    "www.heathcoteandivory.com", "www.flubit.com", "www.wellindulged.com", "www.laganwines.com", "www.chocolates.co.uk",
    "www.guitarcenter.com", "www.musiciansfriend.com", "www.sweetwater.com", "www.thomann.de", "www.samash.com",
    "www.paradigm.com", "www.sonos.com", "www.platinumtools.com", "www.guitarworld.com", "www.turntablelab.com",
    "www.samsung.com", "www.lg.com", "www.sony.com", "www.sharp.com", "www.panasonic.com", "www.vizio.com", "www.tcl.com",
    "www.bose.com", "www.marshallheadphones.com", "www.fender.com", "www.xbox.com", "www.playstation.com", "www.nintendo.com",
    "www.monoprice.com", "www.canary.com", "www.nest.com", "www.ring.com", "www.philips.com", "www.vtechphones.com",
    "www.harman.com", "www.logitech.com", "www.revit.com", "www.filament.io", "www.siemens.com", "www.bosch.com",
    "www.cisco.com", "www.dell.com", "www.compaq.com", "www.hp.com", "www.lenovo.com", "www.compuplus.com", "www.cdw.com",
    "www.newegg.com", "www.tigerdirect.com", "www.microcenter.com", "www.pconline.com", "www.frys.com",
    "www.hitachi.com", "www.acer.com", "www.intel.com", "www.asus.com", "www.apple.com", "www.samsung.com",
    "www.microsoft.com", "www.dell.com", "www.compaq.com", "www.hpe.com", "www.seagate.com", "www.western-digital.com",
    "www.toshiba.com", "www.sandisk.com", "www.kingston.com", "www.lexar.com", "www.patriotmemory.com", "www.crucial.com",
    "www.logitech.com", "www.razer.com", "www.coolermaster.com", "www.nzxt.com", "www.corsair.com", "www.antec.com",
    "www.thermaltake.com", "www.coolermaster.com", "www.bykski.com", "www.thermaltake.com", "www.innocooling.com",
    "www.alienware.com", "www.corsair.com", "www.asus.com", "www.dell.com", "www.microsoft.com", "www.hp.com", "www.lenovo.com",
    "www.lenovo.com", "www.alienware.com", "www.komodo.com", "www.gotomarket.com", "www.freelancer.com", "www.truelancer.com",
    "www.upwork.com", "www.peopleperhour.com", "www.guru.com", "www.toptal.com", "www.freelancer.com", "www.99designs.com",
    "www.fiverr.com", "www.hired.com", "www.glassdoor.com", "www.indeed.com", "www.jobvite.com", "www.workable.com",
    "www.careers360.com", "www.ziprecruiter.com", "www.angellist.com", "www.jobsearch.com", "www.breezy.hr", "www.workday.com",
    "www.monster.com", "www.recruiter.com", "www.lever.co", "www.workmarket.com", "www.jobstreet.com", "www.seek.com.au",
    "www.stepstone.com", "www.reed.co.uk", "www.totaljobs.com", "www.jobrapido.com", "www.jobserve.com", "www.jobisjob.com"
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

        try:
            scraped_data = scrape_by_url(product_url)
            if not scraped_data or "error" in scraped_data:
                return Response({"error": scraped_data.get("error", "Couldn't fetch product data!")}, status=HTTP_400_BAD_REQUEST)
            reviews = scraped_data.get('reviews',[])
            sentimen_reviews=[]
            positive_rev=0
            neg_rev=0
            answer = ""
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
            if total_reviews <= 3:
                answer = "Suspicious Product"
            elif positive_rev > neg_rev:
                answer = "Genuine Product"
            else:
                answer = "Suspicious Product"
            product = StoreURLDetailsModel.objects.create(
                user=request.user,
                title=scraped_data.get("title", ""),
                Product_URL=product_url,
                description=scraped_data.get("description", ""),
                reviews=reviews,
                sentiment = answer
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
                "sentiment": answer
            }, status=HTTP_201_CREATED)

        except Exception as err:
            return Response({"error": str(err)}, status=HTTP_400_BAD_REQUEST)