# Generated by Django 2.2 on 2020-03-26 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_comment_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='likes',
            field=models.ManyToManyField(related_name='likes', to='app.User'),
        ),
    ]
