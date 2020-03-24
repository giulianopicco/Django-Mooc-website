# Generated by Django 2.1.5 on 2019-06-25 21:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_answer'),
    ]

    operations = [
        migrations.CreateModel(
            name='MultipleChoiceQuestion',
            fields=[
                ('question_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='courses.Question')),
                ('shuffle_anwsers', models.BooleanField(default=False)),
            ],
            bases=('courses.question',),
        ),
    ]
