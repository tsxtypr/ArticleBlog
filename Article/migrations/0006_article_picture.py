# Generated by Django 2.2.1 on 2019-09-16 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Article', '0005_auto_20190916_1004'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='picture',
            field=models.ImageField(default='images/01.jpg', upload_to='images'),
            preserve_default=False,
        ),
    ]
