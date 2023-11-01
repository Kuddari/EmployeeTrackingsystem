from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class Indicator(models.Model):
    indicator = models.TextField(default='None')
    unitsfordeans = models.PositiveIntegerField(
        default=0,  # Set default value to 0
        validators=[
            MinValueValidator(0),  # Minimum value
            MaxValueValidator(100)  # Maximum value (adjust as needed)
        ]
    )
    unitsforlecturers = models.PositiveIntegerField(
        default=0,  # Set default value to 0
        validators=[
            MinValueValidator(0),  # Minimum value
            MaxValueValidator(100)  # Maximum value (adjust as needed)
        ]
    )
    unitsforemployees = models.PositiveIntegerField(
        default=0,  # Set default value to 0
        validators=[
            MinValueValidator(0),  # Minimum value
            MaxValueValidator(100)  # Maximum value (adjust as needed)
        ]
    )
    

    def __str__(self):
        return f"{self.indicator}"

class Work(models.Model):
    name = models.CharField(max_length=50)
    indicator = models.ManyToManyField(Indicator)
    
    def __str__(self):
        return f"{self.name}"

    
    
class Employee(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    POSITION_CHOICES = [
        ('Dean', 'Dean'),
        ('Lecturer', 'Lecturer'),
        ('Researcher', 'Researcher'),
    ]
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)

    def __str__(self):
        return f"{self.username}"


class WorkUnit(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    workname = models.ForeignKey(Work, on_delete=models.CASCADE)
    unit = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.employee} - {self.workname} - {self.unit}" 
    
class Term(models.Model):
    term_name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()

    def is_current_term(self):
        current_date = timezone.now().date()
        return self.start_date <= current_date <= self.end_date
    

class Attachment(models.Model):
    # result = models.ForeignKey(Result, on_delete=models.CASCADE)
    file = models.FileField(upload_to='attachments/')



class Result(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    work = models.ForeignKey(WorkUnit, on_delete=models.CASCADE)
    term1 = models.PositiveIntegerField(default=0)
    term2 = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)
    attachments = models.ManyToManyField(Attachment, editable=False)

    def save(self, *args, **kwargs):
        # Calculate the total before saving
        self.total = self.term1 + self.term2
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.employee} - {self.work}"
    
class savedata (models.Model):
    username = models.ForeignKey(Result, on_delete=models.CASCADE)
    attachments = models.ManyToManyField(Attachment)


