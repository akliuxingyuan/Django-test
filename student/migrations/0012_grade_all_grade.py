# Generated by Django 3.1.7 on 2021-04-23 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0011_paper_countdown'),
    ]

    operations = [
        migrations.AddField(
            model_name='grade',
            name='all_grade',
            field=models.IntegerField(default=10),
            preserve_default=False,
        ),
    ]
