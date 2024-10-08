# Generated by Django 5.0 on 2024-09-04 13:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InviteType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30, verbose_name='Nome')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Preço')),
            ],
        ),
        migrations.CreateModel(
            name='InviteSale',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='COD')),
                ('dt_retired', models.DateTimeField(auto_now_add=True, verbose_name='Data de Retirada')),
                ('name_guest', models.CharField(max_length=255, verbose_name='Nome do Convidado')),
                ('doc_guest', models.CharField(max_length=15, verbose_name='Documento do Convidado')),
                ('observation', models.TextField(blank=True, null=True, verbose_name='Observações')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('type_invite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invites_sales.invitetype', verbose_name='Tipo de Convite')),
            ],
            options={
                'verbose_name': 'Convite Vendido',
                'verbose_name_plural': 'Convites Vendidos',
                'ordering': ['dt_retired'],
            },
        ),
    ]
