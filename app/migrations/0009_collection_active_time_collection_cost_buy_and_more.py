# Generated by Django 4.0.4 on 2022-06-06 14:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_products_foto'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='active_time',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='collection',
            name='cost_buy',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='collection',
            name='cost_discount',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='collection',
            name='cost_sell',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='collection',
            name='foto',
            field=models.FileField(blank=True, upload_to='app/static/sets/', verbose_name='Foto'),
        ),
        migrations.AddField(
            model_name='collection',
            name='number',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='collection',
            name='status',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='worker',
            name='contact',
            field=models.CharField(blank=True, default='', max_length=250, verbose_name='contact'),
        ),
        migrations.AddField(
            model_name='worker',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=250, verbose_name='email'),
        ),
        migrations.AddField(
            model_name='worker',
            name='email_check',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='worker',
            name='fathername',
            field=models.CharField(default=1, max_length=256, verbose_name='fathername'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='worker',
            name='firstname',
            field=models.CharField(default=1, max_length=256, verbose_name='firstname'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='worker',
            name='lastname',
            field=models.CharField(default=1, max_length=256, verbose_name='lastname'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='worker',
            name='live',
            field=models.CharField(choices=[('0', 'Faol emas'), ('1', 'Faol')], default='0', max_length=10, verbose_name='faol'),
        ),
        migrations.AddField(
            model_name='worker',
            name='permission',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='worker',
            name='status',
            field=models.CharField(choices=[('0', 'User'), ('1', 'Admin'), ('2', 'SuperAdmin')], default='0', max_length=10, verbose_name='User'),
        ),
        migrations.CreateModel(
            name='ProductSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info', models.TextField(blank=True)),
                ('status', models.IntegerField(blank=True, default=0)),
                ('active_time', models.DateTimeField(auto_now=True, null=True)),
                ('collection', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='productcollection', to='app.collection')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='productset', to='app.products')),
            ],
            options={
                'verbose_name_plural': 'ProductSet',
            },
        ),
    ]
