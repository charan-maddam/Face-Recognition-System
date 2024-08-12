from django.db import models

# Create your models here.
class admin_tables(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    class Meta:
        db_table = 'admin_tables'


class students(models.Model):
    student_id = models.CharField(max_length=40)
    name = models.CharField(max_length=30)
    DOB = models.DateField(max_length=30)
    gender = models.CharField(max_length=30)
    standard = models.CharField(max_length=50)
    Address = models.CharField(max_length=400)
    image = models.ImageField(upload_to='Faces/', default='default_image.jpg')
    class Meta:
        db_table = 'students'

class faculty(models.Model):
    faculty_id = models.CharField(max_length=40)
    name = models.CharField(max_length=30)
    DOB = models.DateField(max_length=30)
    gender = models.CharField(max_length=30)
    qualification = models.CharField(max_length=50)
    address = models.CharField(max_length=400)

    class Meta:
        db_table = 'faculty'
