# Generated by Django 4.0.3 on 2022-06-24 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodapp', '0006_emailfordistribution_alter_comment_content'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Profile',
        ),
    ]