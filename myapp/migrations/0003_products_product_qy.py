# Generated by Django 4.2.1 on 2023-09-03 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_alter_address_uid_alter_cart_uid_alter_cartitem_uid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='product_qy',
            field=models.IntegerField(default=1),
        ),
    ]
