# Generated by Django 3.1.7 on 2021-03-11 16:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventario_app', '0006_auto_20210311_1013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iteminventario',
            name='conta_contabil',
            field=models.DecimalField(decimal_places=3, max_digits=5, null=True, verbose_name='Conta contábil'),
        ),
        migrations.AlterField(
            model_name='iteminventario',
            name='data_aquisicao',
            field=models.DateField(null=True, verbose_name='Data Aquisição'),
        ),
        migrations.AlterField(
            model_name='iteminventario',
            name='data_ateste',
            field=models.DateField(null=True, verbose_name='Data Ateste'),
        ),
        migrations.AlterField(
            model_name='iteminventario',
            name='descricao',
            field=models.TextField(null=True, verbose_name='descrição'),
        ),
        migrations.AlterField(
            model_name='iteminventario',
            name='empenho',
            field=models.IntegerField(null=True, verbose_name='Empenho'),
        ),
        migrations.AlterField(
            model_name='iteminventario',
            name='fornecedor',
            field=models.CharField(max_length=18, null=True, verbose_name='Fornecedor'),
        ),
        migrations.AlterField(
            model_name='iteminventario',
            name='numero_documento',
            field=models.IntegerField(null=True, verbose_name='Nº Documento'),
        ),
        migrations.AlterField(
            model_name='iteminventario',
            name='responsavel',
            field=models.CharField(max_length=255, null=True, verbose_name='responsável'),
        ),
        migrations.AlterField(
            model_name='iteminventario',
            name='setor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inventario_app.setor'),
        ),
        migrations.AlterField(
            model_name='iteminventario',
            name='usuario_conferencia',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Conferido por'),
        ),
        migrations.AlterField(
            model_name='iteminventario',
            name='valor',
            field=models.DecimalField(decimal_places=3, max_digits=5, null=True, verbose_name='Valor R$'),
        ),
    ]
