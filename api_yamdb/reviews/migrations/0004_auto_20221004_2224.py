# Generated by Django 2.2.16 on 2022-10-04 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_auto_20221004_2208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(default='', max_length=6, verbose_name='Код подтверждения'),
        ),
    ]
