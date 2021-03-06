"""formproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from firstapp import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    # path('',views.index,name="index"),
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('landing/',views.form_name_view,name="form_name"),
    path('login/',views.login_as_view,name="login"),
    path('signup/',views.signup_as_view,name="signup"),
    path('user_signup/',views.user_signup,name="user_signup"),
    path('user_login/',views.user_login,name="user_login"),
    path('information/',views.information_as_view,name="information"),
    path('review_handler',views.review_handler,name="review_handler"),
    path('info_handler',views.add_extra_info,name="info_handler"),

    # path('submit_review/',views.submit_and_display_review,name="submit_review"),
    path('adminlogin/',views.adminlogin_as_view,name="adminlogin"),
    path('adminfirstpage/',views.adminfirstpage_as_view,name="adminfirstpage"),
    path('adminfeedback/',views.adminfeedback_as_view,name="adminfeedback"),
    path('adminpending/',views.adminpending_as_view,name="adminpending"),
    path('adminapproved/',views.adminapproved_as_view,name="adminapproved"),
    path('admin_search_req/',views.admin_search_req,name="admin_search_req"),
    path('scan_recpt/',views.scan_recipt_as_view,name="scan_recpt"),





]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
