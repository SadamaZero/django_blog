# Generated by Django 2.0.3 on 2018-04-01 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_blog', '0004_blog_read_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='last_update',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
