"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    
    path('aboutus.html',  views.aboutus , name='aboutus'),
    path('fake.html',views.fake,name='fake'),
    path('result',views.result,name='result'),
    path('result2',views.result2,name = 'result2'),
    path('graph.html',views.graph,name='graph'),
    path('line_graph.html',views.graph1,name = 'graph1'),
    path('login', views.handeLogin, name="handleLogin"),
    path('logout', views.handelLogout, name="handleLogout"),
    path('signup',views.handleSignUp,name='handleSignup'),
    path('index.html', views.index , name='index2'),
    path('static.html',views.static,name = 'static'),
    path('eda.html',views.eda,name='eda'),
    path('cluster.html',views.cluster,name='cluster'),
    path('correlation.html',views.correlation,name = 'correlation'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)