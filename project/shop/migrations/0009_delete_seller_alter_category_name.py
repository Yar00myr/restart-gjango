# Generated by Django 5.1.7 on 2025-06-23 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_alter_cartitem_unique_together'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Seller',
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
