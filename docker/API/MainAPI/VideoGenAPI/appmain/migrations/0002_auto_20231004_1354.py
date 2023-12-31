# Generated by Django 3.2.15 on 2023-10-04 13:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appmain', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField()),
                ('text', models.TextField()),
                ('audio', models.FileField(blank=True, upload_to='audio/')),
                ('image', models.ImageField(blank=True, upload_to='images/')),
                ('video', models.FileField(blank=True, upload_to='videos/')),
            ],
        ),
        migrations.RemoveField(
            model_name='project',
            name='channel',
        ),
        migrations.DeleteModel(
            name='Channel',
        ),
        migrations.AddField(
            model_name='clip',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appmain.project'),
        ),
    ]
