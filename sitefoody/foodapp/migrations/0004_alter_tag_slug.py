# Generated by Django 4.0.3 on 2022-05-27 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodapp', '0003_alter_profile_options_tag_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(default=1, max_length=100, unique=True),
            preserve_default=False,
        ),
    ]