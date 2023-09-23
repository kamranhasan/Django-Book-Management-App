from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    collaborators = models.ManyToManyField(User, related_name='collaborating_books', blank=True)

class Section(models.Model):
    title = models.CharField(max_length=255)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='sections')
    parent_section = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='child_sections')

class Subsection(models.Model):
    title = models.CharField(max_length=255)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='subsections')