# Generated by Django 5.1.3 on 2025-01-05 07:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cabin', '0008_remove_gallerycollection_image_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gallerycollection',
            name='images',
        ),
        migrations.RemoveField(
            model_name='cabin',
            name='Gallery',
        ),
        migrations.DeleteModel(
            name='GalleryImage',
        ),
        migrations.DeleteModel(
            name='GalleryCollection',
        ),
    ]