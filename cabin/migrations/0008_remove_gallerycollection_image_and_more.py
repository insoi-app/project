# Generated by Django 5.1.3 on 2025-01-05 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cabin', '0007_alter_galleryimage_name_gallerycollection_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gallerycollection',
            name='image',
        ),
        migrations.AddField(
            model_name='gallerycollection',
            name='images',
            field=models.ManyToManyField(related_name='collections', to='cabin.galleryimage'),
        ),
    ]