from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    website = models.URLField()
    about = models.CharField(max_length=200)
    image = models.FileField(upload_to='colImg')
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Student(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    qual = models.CharField(max_length=20)
    adrs = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=50)


class SubCat(models.Model):
    name = models.CharField(max_length=50)
    cat = models.ForeignKey(Category, on_delete=models.CASCADE)


class Job(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    subcat = models.ForeignKey(SubCat, on_delete=models.CASCADE)
    cutoff = models.CharField(max_length=50)
    desc = models.CharField(max_length=200, null=True)


class Question(models.Model):
    question = models.CharField(max_length=200)
    o1 = models.CharField(max_length=200)
    o2 = models.CharField(max_length=200)
    o3 = models.CharField(max_length=200)
    o4 = models.CharField(max_length=200)
    ans = models.CharField(max_length=200)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True)


class Exam(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True)
    mark = models.CharField(max_length=200)
    result = models.CharField(max_length=500, null=True)
    result2 = models.CharField(max_length=500, null=True)
    video = models.FileField(upload_to="Exam", null=True)


class Feedback(models.Model):
    date = models.DateField(auto_now_add=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    feedback = models.CharField(max_length=200)
