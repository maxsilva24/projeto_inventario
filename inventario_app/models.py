from django.db import models
from django.contrib.auth.admin import User

# Create your models here.
class Setor(models.Model):
    sigla =  models.SlugField(max_length=7)

class ItemInventario(models.Model):
    item_conferido =  models.BooleanField()
    descricao = models.TextField()
    tombo = models.IntegerField()
    valor = models.DecimalField(verbose_name='Valor R$', max_digits=5, decimal_places=3)
    conta_contabil = models.DecimalField(verbose_name='Conta contábil', max_digits=5, decimal_places=3)
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE)
    empenho = models.IntegerField()
    fornecedor = models.CharField(max_length=18)
    numero_documento = models.IntegerField()
    data_aquisicao = models.DateField()
    data_ateste = models.DateField()
    dependencia = models.CharField(max_length=255)
    responsavel = models.CharField(max_length=255)
    #campos Extras
    data_importacao =  models.DateTimeField(auto_now_add=True)
    usuario_conferencia = models.ForeignKey(User, on_delete=models.CASCADE)
    