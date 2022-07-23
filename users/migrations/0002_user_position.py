# Generated by Django 4.0.2 on 2022-07-23 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='position',
            field=models.IntegerField(choices=[(1, 'Global Supply Chain Lead'), (2, 'Global Supply Chain Planning Specialist')], default=2, verbose_name='position'),
        ),
    ]