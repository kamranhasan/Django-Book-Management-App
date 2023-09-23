# Generated by Django 4.1.5 on 2023-09-23 12:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_section_parent_section'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='section',
            name='parent_section',
        ),
        migrations.AddField(
            model_name='subsection',
            name='parent_subsection',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child_sections', to='books.subsection'),
        ),
    ]
