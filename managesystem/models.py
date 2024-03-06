from django.contrib.auth.models import User
from django.db import models


class Employee(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    POSITION_CHOICES = [
        ('Dean', 'Dean'),
        ('Lecturer', 'Lecturer'),
        ('Researcher', 'Researcher'),
    ]

    BRANCH_CHOICES = [
        ('IT', 'IT'),
        ('RD', 'RD'),
        ('DS', 'DS'),
    ]
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)
    branch = models.CharField(max_length=50, choices = BRANCH_CHOICES)
    profile = models.FileField(upload_to='profile/', blank=True, null=True)
        
    def __str__(self):
        return f"{self.id} - {self.username.first_name} {self.username.last_name} - {self.position}"
    class Meta:
        verbose_name_plural = "พนักงาน"
    
class Work(models.Model):
    name = models.CharField(max_length=100) ### col for กิจกรรม
    description = models.TextField() ### col for ตัวชี่วัด

    def __str__(self):
        return f"{self.name} - {self.description}"

    class Meta:
        verbose_name_plural = "งาน"
    
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
    
    class Meta:
        verbose_name_plural = "ค่าประเมิณแต่ละเทอม"

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/username/filename
    return f'{instance.employee.username.first_name}_{instance.employee.username.last_name}/{filename}'

class Result(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    work = models.ForeignKey(Setunit, on_delete=models.CASCADE)
    term1 = models.PositiveIntegerField(default=0)
    term2 = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)
    employee_score = models.FloatField(default=0.0)
    dean_score = models.FloatField(default=0.0)
    result_score = models.FloatField(default=0.0)
    file = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    # upload_time = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Calculate the total before saving
        self.total = self.term1 + self.term2
        self.result = self.total * self.dean_score
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.employee} - {self.work}"

    class Meta:
        verbose_name_plural = "ผลลัพธ์แต่ละปี"
    


class Save(models.Model):
    employee_id = models.CharField(max_length=30)
    employee_firstname = models.CharField(max_length=30)
    employee_lastname = models.CharField(max_length=30)
    work = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    total = models.PositiveIntegerField(default=0)
    employee_score = models.FloatField(default=0.0)
    dean_score = models.FloatField(default=0.0)
    result_score = models.FloatField(default=0.0)

    file = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.result = self.total * self.dean_score
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.date} {self.employee_firstname} {self.employee_lastname} - {self.work} - {self.description}"

    class Meta:
        verbose_name_plural = "บันทึกข้อมูล"

class Evaluation(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    evaluation_score = models.FloatField()
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.date} - {self.employee} - {self.evaluation_score}"

    class Meta:
        verbose_name_plural = "สรุปข้อมูล"









