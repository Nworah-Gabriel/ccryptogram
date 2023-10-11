
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from cryptobitsapp import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.userlogin, name="login"),
    path('signup/', views.signup, name="signup"),


    path('activate/<uidb64>/<token>', views.VerificationView.as_view(), name = "activate"),
    path('logout/', views.userlogout, name="logout"),
    path('detail/', views.detail, name="detail"),
    path('signup/', views.signup, name="signup"),
    path('contact/', views.contact, name="contact"),
    path('about/', views.about, name="about"),
    path('signupextra/', views.signupextra, name="signupextra"),
    path('profile/', views.profile, name="profile"),
    path('testimony/', views.testimony, name="testimony"),
    path('test/', views.test, name="test"),
    path('', views.index, name=""),
    path('index', views.index, name="index"),
    path('faq', views.faq, name="faq"),
    path('withdraw', views.withdraw, name="withdraw"),
    path('deposit', views.deposit, name="deposit"),
    path('profile/withdraw', views.withdraw, name="withdraw"),
    path('profile/deposit', views.deposit, name="deposit"),
    path('blog/', views.blog, name="blog"),
    path('error/', views.error, name="error")

]
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)