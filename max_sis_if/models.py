from django.db import models
from django.contrib.auth.admin import User, UserAdmin
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField 

# Create your models here.
class Setor(models.Model):
    class Meta:
        verbose_name = 'Setor'
        verbose_name_plural ='Setores'

    sigla =  models.SlugField(max_length=7, verbose_name='Sigla')
    nome =  models.SlugField(max_length=7, verbose_name='Nome Setor', null=True, blank=True)
    observacao = RichTextField(verbose_name='Observação', null=True, blank=True)
    def __str__(self):
        if self!= None:
            if self.sigla!= None and len(self.sigla) > 0 :
                return self.sigla
        return super().__str__()

class Dependencia(models.Model):
    class Meta:
        verbose_name = 'Dependência'
        verbose_name_plural ='Dependências'
    nome_dependencia= models.CharField(max_length=255,verbose_name='Nome da Dependência')
    descricao_local = RichTextUploadingField(verbose_name='Descrição do Local',null=True, blank=True)
    observacao = RichTextField(verbose_name='Observação',null=True, blank=True,)
    def __str__(self):
        return self.nome_dependencia
class ItemInventario(models.Model):
    
    class Meta:
        verbose_name = 'Item do Inventário'
        verbose_name_plural ='Itens do Inventário'
    tombo = models.IntegerField(verbose_name='Tombo', null=True)
    descricao = models.TextField(verbose_name='descrição',null=True)    
    item_conferido =  models.BooleanField(verbose_name='Item Conferido?', null=True)
    usuario_conferencia = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Conferido por', null=True)
    dependencia_atual = models.ForeignKey(Dependencia, on_delete=models.CASCADE, verbose_name='Dependência Atual',null=True,blank=True, related_name='dependencia_atual')
    dependencia_conferencia = models.ForeignKey(Dependencia, on_delete=models.CASCADE, verbose_name='Dependência Conferência',null=True,blank=True, related_name='dependencia_conferencia')
    observacao = RichTextUploadingField(verbose_name='Observação',null=True, blank=True)
    data_conferencia =  models.DateTimeField(verbose_name='Data Últ. Conferência',auto_now=True)
    # 
    valor = models.DecimalField(verbose_name='Valor R$', max_digits=9, decimal_places=2,null=True)
    conta_contabil = models.IntegerField(verbose_name='Conta contábil',null=True)
    setor_atual = models.ForeignKey(Setor, on_delete=models.CASCADE,verbose_name='Setor Atual',null=True, blank=True, related_name='setor_atual')
    setor_conferencia = models.ForeignKey(Setor, on_delete=models.CASCADE,verbose_name='Setor Conferência',null=True, blank=True, related_name='setor_conferencia')
    empenho = models.IntegerField(verbose_name='Empenho',null=True)
    fornecedor = models.CharField(verbose_name='Fornecedor', max_length=18,null=True)
    numero_documento = models.IntegerField(verbose_name='Nº Documento',null=True)
    data_aquisicao = models.DateField(verbose_name='Data Aquisição',null=True)
    data_ateste = models.DateField(verbose_name='Data Ateste',null=True)
    responsavel = models.CharField(verbose_name='responsável',max_length=255,null=True)
    #campos Extras
    data_importacao =  models.DateTimeField(verbose_name='Data Importação/Criação',auto_now_add=True)

   
    def __str__(self):
        if self!= None:
            if self.descricao!= None and len(self.descricao) > 0 :
                return self.descricao[:50]
        return super().__str__()
    

    