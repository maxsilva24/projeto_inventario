# Generated by Django 3.1.7 on 2021-03-11 12:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventario_app', '0003_auto_20210311_0857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iteminventario',
            name='dependencia',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inventario_app.dependencia', verbose_name='Dependência'),
        ),
    ]
