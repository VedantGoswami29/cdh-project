from django.db import models
import hashlib
import os
from django.utils.timezone import now
from datetime import datetime

# Create your models here.

def rename_file_student(instance, file_name):
    extension = file_name.split(".")[-1]
    hashed_name = hashlib.sha256(f"{instance.first_name} {instance.last_name} - {instance.start_year}-{instance.parrent_mobile_number}".encode()).hexdigest()
    new_name = f"{hashed_name}.{extension}"
    return os.path.join("student",new_name)

def rename_file_document(instance, file_name):
    extension = file_name.split(".")[-1]
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    hashed_name = hashlib.sha256(f"{instance.student.first_name} {instance.student.last_name} - {instance.document_name} - {current_time}".encode()).hexdigest()
    new_name = f"{hashed_name}.{extension}"
    return os.path.join("document",new_name)

class Student(models.Model):
    group_choices = [
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
    ]
    type_choices = [
        ('Regular', 'Regular'),
        ('Only NEET/JEE', 'Only NEET/JEE'),
        ('Repeater', 'Repeater'),
    ]
    status_choices = [
        ('Studying','Studying'),
        ('Not Studying','Not Studying'),
        ('Completed','Completed'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to=rename_file_student)
    group = models.CharField(max_length=2, choices=group_choices)
    standard = models.CharField(max_length=255, default=11)
    start_year = models.CharField(max_length=4)
    student_type = models.CharField(max_length=50, choices=type_choices)
    roll_number = models.CharField(max_length=10, unique=True)
    birth_date = models.DateField(default=now)
    student_mobile_number = models.CharField(default=None, max_length=255)
    parrent_mobile_number = models.CharField(default=None, max_length=255)
    discussed_fee = models.IntegerField()
    remaining_fees = models.IntegerField()
    status = models.CharField(default="Studying", choices=status_choices, max_length=255)
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.start_year}"

class StudentDocument(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    document_name = models.CharField(max_length=255)
    document = models.FileField(upload_to=rename_file_document)
    upload_time = models.DateTimeField(default=now)


    @property
    def student_name(self):
        return f"{self.student.first_name} {self.student.last_name}"
    
    def __str__(self) -> str:
        return f"{self.student.first_name} {self.student.last_name} - {self.document_name}"
    