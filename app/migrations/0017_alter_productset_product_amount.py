# Generated by Django 4.0.4 on 2022-06-13 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_remove_products_amount_one_pack_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productset',
            name='product_amount',
            field=models.IntegerField(blank=True, default=1),
        ),
    ]
