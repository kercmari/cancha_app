# Generated by Django 5.0.6 on 2024-06-29 16:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Reserva', '0002_persona_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='persona',
            name='user',
        ),
    ]