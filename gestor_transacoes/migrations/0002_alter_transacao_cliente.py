# Generated by Django 4.2.17 on 2024-12-10 21:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestor_transacoes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transacao',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transacao', to='gestor_transacoes.cliente', to_field='cpf', verbose_name='Cliente (CPF)'),
        ),
    ]
