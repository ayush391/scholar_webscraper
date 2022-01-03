# Generated by Django 4.0 on 2021-12-17 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Authors',
            fields=[
                ('author_id', models.AutoField(primary_key=True, serialize=False)),
                ('author_name', models.CharField(max_length=100)),
                ('scholar_link', models.CharField(max_length=1000)),
                ('pfp_link', models.CharField(max_length=1000)),
            ],
        ),
    ]