# Generated by Django 4.1.7 on 2023-03-31 04:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wb', '0025_alter_resposta_resposta'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='boaspraticas',
            options={'verbose_name': 'BoasPraticas', 'verbose_name_plural': 'Boas Praticas'},
        ),
        migrations.AlterModelOptions(
            name='empresa',
            options={'verbose_name': 'Empresa', 'verbose_name_plural': 'Empresas'},
        ),
        migrations.AlterModelOptions(
            name='estrategiacircular',
            options={'verbose_name': 'EstrategiaCircular', 'verbose_name_plural': 'Estrategias Circulares'},
        ),
        migrations.AlterModelOptions(
            name='questionario',
            options={'verbose_name': 'Questionario', 'verbose_name_plural': 'Questionarios'},
        ),
        migrations.AlterModelOptions(
            name='resposta',
            options={'verbose_name': 'Resposta', 'verbose_name_plural': 'Respostas'},
        ),
        migrations.AlterModelOptions(
            name='segmento',
            options={'verbose_name': 'Segmento', 'verbose_name_plural': 'Segmentos'},
        ),
        migrations.AlterModelOptions(
            name='targetgrafico',
            options={'verbose_name': 'TargetGrafico', 'verbose_name_plural': 'Targets do Gráfico'},
        ),
        migrations.AlterModelOptions(
            name='valorreferencia',
            options={'verbose_name': 'ValorReferencia', 'verbose_name_plural': 'Valores de Referencia'},
        ),
        migrations.CreateModel(
            name='ReferenciaPessoal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resposta', models.DecimalField(decimal_places=10, max_digits=20)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wb.empresa')),
                ('questao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wb.questionario')),
            ],
            options={
                'verbose_name': 'Referencia Pessoal',
                'verbose_name_plural': 'Referencias Pessoais',
            },
        ),
    ]
