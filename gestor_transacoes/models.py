from django.db import models
from django.core.exceptions import ValidationError

class Cliente(models.Model):
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF")
    email = models.EmailField(max_length=255, verbose_name="E-mail")
    telefone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.nome} - ({self.cpf})"
    
    def delete(self, *args, **kwargs):
        if self.transacao.exists():
            raise ValidationError("Não é possível excluir um cliente com transações associadas.")
        super().delete(*args, **kwargs)
    
    
class Transacao(models.Model):
    CATEGORIAS = [
        ('alimentacao', 'Alimentacao'),
        ('transporte', 'Transporte'),
        ('lazer', 'Lazer'),
        ('outros', 'Outros')
    ]

    cliente =  models.ForeignKey(
        Cliente, 
        on_delete=models.CASCADE, 
        related_name='transacao', 
        to_field='cpf', 
        verbose_name='Cliente (CPF)'
    )
    data_hora =  models.DateTimeField(auto_now_add=True, verbose_name="Data e Hora")
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField()
    categoria = models.CharField(max_length=50, choices=CATEGORIAS)

    def clean(self):
        super().clean()
        if self.valor == 0:
            raise ValidationError("O valor da transação deve ser diferente de zero.")
        
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)