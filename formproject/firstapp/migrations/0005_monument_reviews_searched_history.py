# Generated by Django 2.1.5 on 2020-02-18 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0004_user_data_gender'),
    ]

    operations = [
        migrations.CreateModel(
            name='monument_reviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=264)),
                ('monument_name', models.CharField(max_length=264)),
                ('user_review', models.CharField(max_length=264)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='searched_history',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=264)),
                ('monument_name', models.CharField(max_length=264)),
            ],
        ),
    ]