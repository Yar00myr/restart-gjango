# Generated by Django 5.1.7 on 2025-04-24 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_order_contact_phone_alter_order_contact_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='provider',
            field=models.CharField(choices=[('liqpay', 'LiqPay'), ('monopay', 'MonoPay'), ('google', 'Google Pay')], max_length=20),
        ),
    ]
