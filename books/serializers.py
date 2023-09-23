from rest_framework import serializers
from .models import Book, Section, Subsection

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'
        extra_kwargs = {
            'book': {'required': False}  # Make the book field optional for updates
        }

class SubsectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subsection
        fields = '__all__'
        extra_kwargs = {
            'section': {'required': False}  # Make the section field optional for updates
        }