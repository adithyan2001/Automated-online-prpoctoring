"""SkillPoint URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from spApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.CommonHome, name='CommonHome'),
    path('SignIn/', views.SignIn, name='Sign In'),
    path('CompanySignup/', views.CompanySignup, name='CompanySignup'),
    path('StudentSignup/', views.StudentSignup, name='StudentSignup'),




    path('AdminHome/', views.AdminHome, name='AdminHome'),
    path('AdminViewCompany/', views.AdminViewCompany, name='AdminViewCompany'),
    path('AdminViewStudents/', views.AdminViewStudents, name='AdminViewStudents'),
    path('AdminViewFeedback/', views.AdminViewFeedback, name='AdminViewFeedback'),
    path('AdminCategory/', views.AdminCategory, name='AdminCategory'),
    path('AdminSubcategory/', views.AdminSubcategory, name='AdminSubcategory'),
    path('viewAllQuestions/', views.viewAllQuestions, name='viewAllQuestions'),
    path('editQuestion/', views.editQuestion, name='editQuestion'),




    path('CompanyHome/', views.CompanyHome, name='CompanyHome'),
    path('CompanyPrepareQuestion/', views.CompanyPrepareQuestion,
         name='CompanyPrepareQuestion'),
    path('CompanyViewJobcode/', views.CompanyViewJobcode,
         name='CompanyViewJobcode'),
    path('CompanyViewExamResult/', views.CompanyViewExamResult,
         name='CompanyViewExamResult'),
    path('CompanyCourse/', views.CollegeCourse, name='CompanyCourse'),



    path('StudentHome/', views.StudentHome, name='StudentHome'),
    path('StudentFindJob/', views.StudentFindJob, name='StudentFindJob'),
    path('StudentViewJobs/', views.StudentViewJobs, name='StudentViewJobs'),

    path('StudentAttentAptitudeTest/', views.StudentAttentAptitudeTest,
         name='StudentAttentAptitudeTest'),
    path('StudentViewQuestions/', views.StudentViewQuestions,
         name='StudentViewQuestions'),
    path('StudentViewMarksAnswer/', views.StudentViewMarksAnswer,
         name='StudentViewMarksAnswer'),
    path('CustomerAddFeedback/', views.CustomerAddFeedback,
         name='CustomerAddFeedback'),
    path('StudentViewCompany/', views.StudentViewCollege,
         name='StudentViewCompany'),
    path('StudentTest/', views.StudentTest, name='StudentTest'),
    path('StudentPossibleCompany/', views.StudentPossibleCollege,
         name='StudentPossibleCompany'),
    path("eval", views.eval),
    path('stuQus/', views.stuQus,
         name='stuQus'),


]
