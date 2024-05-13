"""
URL configuration for djashopping project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from pig.views import pig
from chicken.views import chicken
from beef.views import beef
from mutton.views import mutton
from seafood.views import seafood
from member.views import register,login,logout
from contact.views import contact
from about.views import aboutme
from cart.views import cart,addtocart,cartorder,cartok,cartordercheck,myOrder,reportBank,ECPayCredit,bankfive


urlpatterns = [
    path('admin/', admin.site.urls),
    path("pig/",pig),
    path("chicken/",chicken),
    path("beef/",beef),
    path("mutton/",mutton),
    path("seafood/",seafood),
    path('register/',register),
    path('login/',login),
    path('logout/',logout),
    path("contact/",contact),
    path("about/",aboutme),
    path('addtocart/<str:ctype>/<int:pigid>/',addtocart),
    path('addtocart/<str:ctype>/',addtocart),
    path('cart/',cart),
    path('cartok/',cartok),
    path('cartorder/',cartorder),
    path('cartordercheck/',cartordercheck),
    path('myorder/',myOrder),
    path('reportBank/',reportBank),
    path('creditcard/',ECPayCredit),
    path('bankfive/',bankfive),    
    path('',aboutme),  
]
