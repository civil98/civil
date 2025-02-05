# Generated by Django 4.2.16 on 2024-11-18 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='document_name',
        ),
        migrations.RemoveField(
            model_name='document',
            name='number',
        ),
        migrations.RemoveField(
            model_name='document',
            name='person_national_name',
        ),
        migrations.AddField(
            model_name='document',
            name='done',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='document',
            name='notes',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='person_national_num',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='second_national_num',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='document_date',
            field=models.DateField(null=True),
        ),
    ]
