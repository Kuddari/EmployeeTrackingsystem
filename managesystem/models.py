from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator




class Employee(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    POSITION_CHOICES = [
        ('Dean', 'Dean'),
        ('Lecturer', 'Lecturer'),
        ('Researcher', 'Researcher'),
    ]
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)
           
    def __str__(self):
        return f"{self.username.first_name} {self.username.last_name} - {self.position}"
    
class Work(models.Model):
    name = models.CharField(max_length=100) ### col for กิจกรรม
    description = models.TextField() ### col for ตัวชี่วัด

    def __str__(self):
        return f"{self.name} - {self.description}"
    
class Setunit(models.Model):
    name = models.ForeignKey(Work,on_delete=models.CASCADE) ### ตำแหน่ง
    minunit = models.PositiveIntegerField(default=0) ### ค่าน้ำหนักตำ
    maxunit = models.PositiveIntegerField(default=0) ### สูง
    POSITION_CHOICES = [
        ('Dean', 'Dean'),
        ('Lecturer', 'Lecturer'),
        ('Researcher', 'Researcher'),
    ]
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)
    def __str__(self):
        return f"{self.id} - {self.position} - {self.name.name} - {self.name.description}"

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/username/filename
    return f'{instance.employee.username.first_name}_{instance.employee.username.last_name}/{filename}'

class Result(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    work = models.ForeignKey(Setunit, on_delete=models.CASCADE)
    term1 = models.PositiveIntegerField(default=0)
    term2 = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)
    result = models.PositiveIntegerField(default=0)
    file = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    # upload_time = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Calculate the total before saving
        self.total = self.term1 + self.term2
        self.result = self.total * self.work.minunit
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.employee} - {self.work}"
    


class Save(models.Model):
    employee_id = models.CharField(max_length=30)
    employee_firstname = models.CharField(max_length=30)
    employee_lastname = models.CharField(max_length=30)
    work = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    unit = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)
    score = models.PositiveIntegerField(default=0)
    file = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Format the date before saving
        self.date = timezone.now().strftime("%d %m %Y")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.date} {self.employee_firstname} {self.employee_lastname} - {self.work} - {self.description}"
    










