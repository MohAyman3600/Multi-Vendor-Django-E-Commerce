# Generated by Django 3.1.1 on 2020-09-16 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='company_website',
            field=models.URLField(max_length=50, verbose_name='company website'),
        ),
    ]
