# Generated by Django 4.0.4 on 2022-04-24 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mqtt', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='name',
            field=models.CharField(db_index=True, max_length=50, unique=True),
        ),
    ]