# Generated by Django 4.2.16 on 2024-12-03 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0013_document_done'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='paid',
            field=models.CharField(default='not paid', max_length=15),
        ),
    ]
