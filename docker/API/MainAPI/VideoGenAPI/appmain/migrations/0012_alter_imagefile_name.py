# Generated by Django 3.2.15 on 2023-10-06 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appmain', '0011_auto_20231006_0638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagefile',
            name='name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]