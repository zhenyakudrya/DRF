# Generated by Django 5.0.2 on 2024-02-19 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='link_video',
            field=models.URLField(verbose_name='ссылка на видео'),
        ),
    ]
