"""loan_demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from loans.views import LoanView, LoanRequestListView, LoanRequestUpdate, LoanRequestDelete
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import views as auth_views
# from django.contrib import admin
from loan_demo import settings

urlpatterns = [
    path('login/', auth_views.login, name='login'),
    path('logout/', auth_views.logout, {'next_page': '/'}, name='logout'),
    path('', LoanView.as_view()),
    path('loans/', staff_member_required(LoanRequestListView.as_view(), login_url=settings.LOGIN_URL)),
    path('loans/<int:pk>/update/', staff_member_required(LoanRequestUpdate.as_view(), login_url=settings.LOGIN_URL)),
    path('loans/<int:pk>/delete/', staff_member_required(LoanRequestDelete.as_view(), login_url=settings.LOGIN_URL)),
]
