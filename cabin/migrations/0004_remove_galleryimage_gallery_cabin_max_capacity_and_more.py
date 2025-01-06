# Generated by Django 5.1.3 on 2025-01-01 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cabin', '0003_gallery_galleryimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='galleryimage',
            name='gallery',
        ),
        migrations.AddField(
            model_name='cabin',
            name='max_capacity',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='cabin',
            name='name',
            field=models.CharField(choices=[('Saro', 'Cabin Saro'), ('Duwa', 'Cabin Duwa'), ('Gabos', 'Cabin Gabos')], max_length=50),
        ),
        migrations.DeleteModel(
            name='Gallery',
        ),
        migrations.DeleteModel(
            name='GalleryImage',
        ),
    ]
