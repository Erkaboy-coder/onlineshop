# Generated by Django 4.0.4 on 2022-06-06 09:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0003_worker'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker',
            name='user',
            field=models.OneToOneField(help_text='User linked to this admin', on_delete=django.db.models.deletion.PROTECT, related_name='admin', to=settings.AUTH_USER_MODEL, verbose_name='Related user'),
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('cost_buy', models.CharField(blank=True, max_length=100, null=True)),
                ('cost_sell', models.CharField(blank=True, max_length=100, null=True)),
                ('discount', models.CharField(blank=True, max_length=100, null=True)),
                ('cost_one', models.CharField(blank=True, max_length=100, null=True)),
                ('cost_all', models.CharField(blank=True, max_length=100, null=True)),
                ('cost_discount_one', models.CharField(blank=True, max_length=100, null=True)),
                ('company', models.CharField(blank=True, max_length=100, null=True)),
                ('foto', models.FileField(blank=True, upload_to='static/photo/', verbose_name='Foto')),
                ('info', models.TextField(blank=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='productcategory', to='app.category')),
            ],
            options={
                'verbose_name_plural': 'Products',
            },
        ),
    ]