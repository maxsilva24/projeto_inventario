# Generated by Django 3.1.7 on 2021-03-12 08:54

import ckeditor.fields
import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dependencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_dependencia', models.CharField(max_length=255, verbose_name='Nome da Dependência')),
                ('descricao_local', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Descrição do Local')),
                ('observacao', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Observação')),
            ],
            options={
                'verbose_name': 'Dependência',
                'verbose_name_plural': 'Dependências',
            },
        ),
        migrations.CreateModel(
            name='Setor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sigla', models.SlugField(max_length=7, verbose_name='Sigla')),
                ('nome', models.SlugField(blank=True, max_length=7, null=True, verbose_name='Nome Setor')),
                ('observacao', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Observação')),
            ],
            options={
                'verbose_name': 'Setor',
                'verbose_name_plural': 'Setores',
            },
        ),
        migrations.CreateModel(
            name='ItemInventario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tombo', models.IntegerField(null=True, verbose_name='Tombo')),
                ('descricao', models.TextField(null=True, verbose_name='descrição')),
                ('item_conferido', models.BooleanField(null=True, verbose_name='Item Conferido?')),
                ('observacao', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Observação')),
                ('data_conferencia', models.DateTimeField(auto_now=True, verbose_name='Data Últ. Conferência')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=9, null=True, verbose_name='Valor R$')),
                ('conta_contabil', models.IntegerField(null=True, verbose_name='Conta contábil')),
                ('empenho', models.IntegerField(null=True, verbose_name='Empenho')),
                ('fornecedor', models.CharField(max_length=18, null=True, verbose_name='Fornecedor')),
                ('numero_documento', models.IntegerField(null=True, verbose_name='Nº Documento')),
                ('data_aquisicao', models.DateField(null=True, verbose_name='Data Aquisição')),
                ('data_ateste', models.DateField(null=True, verbose_name='Data Ateste')),
                ('responsavel', models.CharField(max_length=255, null=True, verbose_name='responsável')),
                ('data_importacao', models.DateTimeField(auto_now_add=True, verbose_name='Data Importação/Criação')),
                ('dependencia_atual', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dependencia_atual', to='max_sis_if.dependencia', verbose_name='Dependência Atual')),
                ('dependencia_conferencia', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dependencia_conferencia', to='max_sis_if.dependencia', verbose_name='Dependência Conferência')),
                ('setor_atual', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='setor_atual', to='max_sis_if.setor', verbose_name='Setor Atual')),
                ('setor_conferencia', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='setor_conferencia', to='max_sis_if.setor', verbose_name='Setor Conferência')),
                ('usuario_conferencia', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Conferido por')),
            ],
            options={
                'verbose_name': 'Item do Inventário',
                'verbose_name_plural': 'Itens do Inventário',
            },
        ),
    ]
