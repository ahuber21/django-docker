# Generated by Django 4.0.4 on 2022-04-24 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fingerprints', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fingerprint',
            name='template_id',
            field=models.IntegerField(default=-1),
            preserve_default=False,
        ),
    ]