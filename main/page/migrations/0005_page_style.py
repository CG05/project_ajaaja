# Generated by Django 5.0.6 on 2024-06-04 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0004_alter_page_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='style',
            field=models.JSONField(default=dict, verbose_name='json'),
        ),
    ]