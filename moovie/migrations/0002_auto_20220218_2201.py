# Generated by Django 2.1.5 on 2022-02-18 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moovie', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='age',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='contactmessage',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='image',
            field=models.ImageField(blank=True, upload_to='movie_images'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='release_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='image',
            field=models.ImageField(blank=True, upload_to='person_images'),
        ),
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]