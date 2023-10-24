from django.db import models
from .models import Attachment
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Work(models.Model):
    name = models.CharField(max_length=100)
    unitsfordeans = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),  # Minimum value
            MaxValueValidator(100)  # Maximum value (adjust as needed)
        ]
    )
    unitsforlecturers = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),  # Minimum value
            MaxValueValidator(100)  # Maximum value (adjust as needed)
        ]
    )
    unitsforemployees = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),  # Minimum value
            MaxValueValidator(100)  # Maximum value (adjust as needed)
        ]
    )
    def __str__(self):
        return f"{self.name}"
    
class Employee(models.Model):
    username = models.CharField(max_length=50)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    POSITION_CHOICES = [
        ('Dean', 'Dean'),
        ('Lecturer', 'Lecturer'),
        ('Researcher', 'Researcher'),
        # Add more choices as needed
    ]
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)
    def __str__(self):
        return f"{self.username}"

class WorkUnit(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    workname = models.ForeignKey(Work, on_delete=models.CASCADE)
    unit = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.employee} - {self.workname} - {self.unit}" 
    
class Term(models.Model):
    term_name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()

    def is_current_term(self):
        current_date = timezone.now().date()
        return self.start_date <= current_date <= self.end_date


class Result(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    work = models.ForeignKey(WorkUnit, on_delete=models.CASCADE)
    term1 = models.PositiveIntegerField(default=0)
    term2 = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0, editable=False)
    attachments = models.ManyToManyField(Attachment)

    def calculate_total_units(self):
        current_term_units = 0

        # Determine the current term and set current_term_units accordingly
        terms = Term.objects.all()
        for term in terms:
            if term.is_current_term():
                if term.term_name == 'term1':
                    current_term_units = self.term1_units
                else:
                    current_term_units = self.term2_units
                break

        if self.work.workname == 'Math':
            # Calculate total units for Math
            self.total_units = current_term_units
        else:
            # Set total_units to the current term's units for other subjects
            self.total_units = self.term1_units + self.term2_units

        self.save()

    def __str__(self):
        return f"{self.employee} - {self.work} - Total Units: {self.total_units}"
    
class Attachment(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE)
    file = models.FileField(upload_to='attachments/')

    

