# Generated by Django 3.2.15 on 2023-10-05 19:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appmain', '0004_rename_imagemodel_imagefile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='imagefile',
            old_name='image',
            new_name='path',
        ),
    ]
