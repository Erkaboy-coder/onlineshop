# Generated by Django 4.0.4 on 2022-06-06 09:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_worker_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='products',
            old_name='cot_discount',
            new_name='cost_discount',
        ),
    ]