from django.db import models
from django.core.exceptions import ValidationError
import re

class Cliente(models.Model):
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF")
    email = models.EmailField(max_length=255, verbose_name="E-mail")
    telefone = models.CharField(max_length=20, blank=True, null=True)
   
    
class Transacao(models.Model):
    CATEGORIAS = [
        ('alimentacao', 'Alimentacao'),
        ('transporte', 'Transporte'),
        ('lazer', 'Lazer'),
        ('outros', 'Outros')
    ]

    cliente =  models.ForeignKey(
        Cliente, 
        on_delete=models.PROTECT, 
        related_name='transacao', 
        to_field='cpf', 
        verbose_name='Cliente (CPF)'
    )
    data_hora = models.DateTimeField(verbose_name="Data e Hora")
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField()
    categoria = models.CharField(max_length=50, choices=CATEGORIAS)
        
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)