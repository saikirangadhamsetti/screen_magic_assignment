# Generated by Django 4.1.4 on 2022-12-30 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emailmessaging', '0005_alter_messages_phone_alter_messages_schedule_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='Phone',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='messages',
            name='Schedule_date',
            field=models.CharField(max_length=20),
        ),
    ]
