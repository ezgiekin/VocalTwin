# Generated by Django 5.1 on 2024-09-06 07:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_voicerecording_text_language'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='voicerecording',
            name='language',
        ),
        migrations.RemoveField(
            model_name='voicerecording',
            name='recording',
        ),
        migrations.RemoveField(
            model_name='voicerecording',
            name='text',
        ),
        migrations.RemoveField(
            model_name='voicerecording',
            name='text_language',
        ),
        migrations.CreateModel(
            name='AudioFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='recordings/')),
                ('recording', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='base.voicerecording')),
            ],
        ),
    ]
