# Generated by Django 3.2.15 on 2023-10-06 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appmain', '0017_auto_20231006_0655'),
    ]

    operations = [
        migrations.RenameField(
            model_name='imagefile',
            old_name='description',
            new_name='prompt',
        ),
        migrations.RemoveField(
            model_name='clip',
            name='index',
        ),
        migrations.AddField(
            model_name='clip',
            name='img_prompt',
            field=models.TextField(default=''),
        ),
    ]
