# Generated by Django 5.1 on 2024-08-12 18:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_alter_groupclass_code_alter_groupclass_max_students'),
    ]

    operations = [
        migrations.DeleteModel(
            name='GroupClass',
        ),
    ]
