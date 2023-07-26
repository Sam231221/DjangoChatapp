# Generated by Django 4.1.1 on 2022-09-19 04:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('MChat', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chatmessage',
            options={'ordering': ('timestamp',)},
        ),
        migrations.AddField(
            model_name='chatmessage',
            name='posted_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]