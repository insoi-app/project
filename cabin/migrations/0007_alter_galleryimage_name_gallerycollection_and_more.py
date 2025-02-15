# Generated by Django 5.1.3 on 2025-01-05 03:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cabin', '0006_remove_galleryimage_description_galleryimage_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='galleryimage',
            name='name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.CreateModel(
            name='GalleryCollection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Saro Gallery', 'Cabin Saro Gallery'), ('Duwa Gallery', 'Cabin Duwa Gallery'), ('Gabos Gallery', 'Cabin Gabos Gallery')], max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cabin.galleryimage')),
            ],
        ),
        migrations.AlterField(
            model_name='cabin',
            name='Gallery',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Cabin', to='cabin.gallerycollection'),
        ),
    ]
