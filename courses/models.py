from django.db import models
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
import uuid
import random

# Create your models here.
class Teacher(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return (self.first_name + ' ' + self.last_name)
    
class Courses(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    teacher=models.ForeignKey(Teacher, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return (self.title)

class Students(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    def __str__(self):
        return (self.first_name + ' ' + self.last_name)

class GroupClass(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=4, unique=True, null=True, blank=True)
    course = models.ForeignKey('Courses', null=True, blank=True, on_delete=models.CASCADE)
    max_students = models.PositiveIntegerField()
    students = models.ManyToManyField('Students', blank=True)

    def save(self, *args, **kwargs):
        if not self.code and self.course:
            first_letter = self.course.title[0].upper()
            random_number = random.randint(1, 100)
            random_number_str = f"{random_number:02}"
            self.code = f"{first_letter}{random_number_str}"[:4]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} - {self.course.title if self.course else 'No Course'}"

# Señal para controlar el límite de estudiantes
@receiver(m2m_changed, sender=GroupClass.students.through)
def limit_students(sender, instance, action, **kwargs):
    if action == "pre_add":  # Antes de agregar estudiantes
        if instance.students.count() + len(kwargs.get('pk_set', [])) > instance.max_students:
            raise ValidationError(f"No se pueden añadir más estudiantes al grupo. El límite máximo es {instance.max_students}.")
        
# class GroupClass(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     code = models.CharField(max_length=4, unique=True, null=True, blank=True)
#     course = models.ForeignKey(Courses, null=True, blank=True, on_delete=models.CASCADE)
#     max_students = models.PositiveIntegerField()
#     students = models.ManyToManyField('Students', blank=True)

#     def save(self, *args, **kwargs):
#         if not self.code and self.course:
#             first_letter = self.course.title[0].upper()
#             random_number = random.randint(1, 100)
#             random_number_str = f"{random_number:02}"
#             self.code = f"{first_letter}{random_number_str}"[:4]

#         super().save(*args, **kwargs)

#         if self.students.count() > self.max_students:
#             raise ValidationError(f"No se pueden añadir más estudiantes al grupo. El límite máximo es {self.max_students}.")

#     def __str__(self):
#         return f"{self.code} - {self.course.title if self.course else 'No Course'}"
    
# class GroupClass(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     code = models.CharField(max_length=4, unique=True, null=True)
#     course = models.ForeignKey(Courses, null=True, blank=True, on_delete=models.CASCADE)
#     max_students = models.PositiveIntegerField()
#     students = models.ManyToManyField(Students, blank=True) 

#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
#         if self.course:
#             first_letter = self.course.title[0].upper()
#             random_number = random.randint(1, 100)
#             random_number_str = f"{random_number:02}"
#             self.code = f"{first_letter}{random_number_str}"
#             self.code = self.code[:4]
#             super().save(*args, **kwargs)

#         if self.pk is not None:
#             existing_group = GroupClass.objects.get(pk=self.pk)
#             current_student_count = self.students.count()
#             if current_student_count > self.max_students:
#                 raise ValidationError(f"No se pueden añadir más estudiantes al grupo. El límite máximo es {self.max_students}.")
#         else: 
#             if self.students.count() > self.max_students:
#                 raise ValidationError(f"No se pueden añadir más estudiantes al grupo. El límite máximo es {self.max_students}.")

#         super().save(*args, **kwargs)
    
#     def __str__(self):
#         return f"{self.code} - {self.course.title if self.course else 'No Course'}"
