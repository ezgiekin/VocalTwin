# Generated by Django 5.1 on 2024-09-03 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_voicerecording_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='voicerecording',
            name='cloned',
            field=models.FileField(default=1, upload_to='cloned_voices/'),
            preserve_default=False,
        ),
    ]
