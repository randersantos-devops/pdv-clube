# Generated by Django 5.0 on 2024-08-31 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invites', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invite',
            name='status_invite',
            field=models.CharField(choices=[('AGREGADO', 'AGREGADO(a)'), ('SINDICALIZADO', 'SINDICALIZADO(A)')], default=('SINDICALIZADO', 'SINDICALIZADO(A)'), max_length=30, verbose_name='Status do Convite'),
        ),
    ]
