# Generated by Django 4.0.3 on 2022-06-01 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodapp', '0005_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailForDistribution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
            ],
            options={
                'verbose_name': 'email',
                'verbose_name_plural': 'emails',
                'ordering': ['id'],
            },
        ),
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(max_length=150),
        ),
    ]
