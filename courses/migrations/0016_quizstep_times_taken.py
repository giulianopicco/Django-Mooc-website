# Generated by Django 2.1.5 on 2020-02-23 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0015_course_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizstep',
            name='times_taken',
            field=models.IntegerField(default=0, editable=False),
        ),
    ]
