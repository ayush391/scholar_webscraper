# Generated by Django 4.0 on 2021-12-19 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler_site', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authors',
            name='author_id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]