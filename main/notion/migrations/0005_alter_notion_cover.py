# Generated by Django 5.0.6 on 2024-06-07 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notion', '0004_alter_notion_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notion',
            name='cover',
            field=models.ImageField(blank=True, upload_to='image/'),
        ),
    ]
