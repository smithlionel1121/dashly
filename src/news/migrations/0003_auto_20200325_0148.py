# Generated by Django 3.0.4 on 2020-03-25 01:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_auto_20200325_0134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='image',
            field=models.ImageField(default='C:/Users/footb/Desktop/Coding/dashly/src/news/static/the-onion-logo.jpg', upload_to=''),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_scrape',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
