from django.urls import path
from . import views
urlpatterns = [
    path('',views.hello,name="hello"),
    path('postURL',views.postURL.as_view(),name="postURL"),
    path('postURL/<int:pk>/delete/',views.DeleteURL.as_view(),name="delete"),
    path('login',views.LoginView.as_view(),name="login"),
    path('register',views.Register.as_view(),name="register"),
    path('scrape/', views.ScrapeURLView.as_view(), name='scrape'),
    path('api/user/',views.CurrentUser.as_view(),name="current_user")
]
