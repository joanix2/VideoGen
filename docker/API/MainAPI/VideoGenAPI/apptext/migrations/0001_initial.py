# Generated by Django 3.2.15 on 2023-10-03 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('appmain', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompletionAgentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_token', models.CharField(max_length=64)),
                ('model', models.CharField(default='gpt-3.5-turbo', max_length=20)),
                ('temperature', models.FloatField(default=0.7)),
                ('max_tokens', models.IntegerField(default=1024)),
                ('n', models.IntegerField(default=1)),
                ('stop', models.TextField(blank=True, null=True)),
                ('presence_penalty', models.FloatField(default=0)),
                ('frequency_penalty', models.FloatField(default=0)),
                ('behavior', models.TextField(blank=True, default='You are a helpful assistant.')),
                ('messages', models.JSONField(blank=True, default=list)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appmain.project')),
            ],
        ),
        migrations.CreateModel(
            name='Clip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField()),
                ('text', models.TextField()),
                ('audio', models.FileField(blank=True, upload_to='audio/')),
                ('image', models.ImageField(blank=True, upload_to='images/')),
                ('video', models.FileField(blank=True, upload_to='videos/')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appmain.project')),
            ],
        ),
    ]
