# Generated by Django 4.0.5 on 2022-10-01 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='content',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]