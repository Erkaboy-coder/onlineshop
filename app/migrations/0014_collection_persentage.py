# Generated by Django 4.0.4 on 2022-06-12 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_productset_product_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='persentage',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]