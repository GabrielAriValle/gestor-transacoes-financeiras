# Generated by Django 4.2.16 on 2024-12-12 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestor_transacoes', '0002_alter_transacao_cliente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transacao',
            name='data_hora',
            field=models.DateTimeField(verbose_name='Data e Hora'),
        ),
    ]
