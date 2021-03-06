# Generated by Django 4.0.4 on 2022-06-06 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_worker_user_products'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='worker',
            options={},
        ),
        migrations.RenameField(
            model_name='products',
            old_name='cost_all',
            new_name='amount_one_pack',
        ),
        migrations.RenameField(
            model_name='products',
            old_name='cost_discount_one',
            new_name='cost_discount_one_pack',
        ),
        migrations.RenameField(
            model_name='products',
            old_name='cost_one',
            new_name='cost_one_pack',
        ),
        migrations.RenameField(
            model_name='products',
            old_name='discount',
            new_name='cot_discount',
        ),
        migrations.RemoveField(
            model_name='worker',
            name='contact',
        ),
        migrations.RemoveField(
            model_name='worker',
            name='email',
        ),
        migrations.RemoveField(
            model_name='worker',
            name='email_check',
        ),
        migrations.RemoveField(
            model_name='worker',
            name='fathername',
        ),
        migrations.RemoveField(
            model_name='worker',
            name='firstname',
        ),
        migrations.RemoveField(
            model_name='worker',
            name='lastname',
        ),
        migrations.RemoveField(
            model_name='worker',
            name='live',
        ),
        migrations.RemoveField(
            model_name='worker',
            name='permission',
        ),
        migrations.RemoveField(
            model_name='worker',
            name='status',
        ),
        migrations.AddField(
            model_name='products',
            name='active_time',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='products',
            name='discount_persents',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='products',
            name='status',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
