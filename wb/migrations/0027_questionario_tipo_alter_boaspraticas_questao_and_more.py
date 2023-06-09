# Generated by Django 4.1.7 on 2023-03-31 04:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wb', '0026_alter_boaspraticas_options_alter_empresa_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionario',
            name='tipo',
            field=models.CharField(choices=[('VA', 'ValorAtingido'), ('VM', 'ValorMeta')], default='VA', max_length=20),
        ),
        migrations.AlterField(
            model_name='boaspraticas',
            name='questao',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='wb.questionario'),
        ),
        migrations.AlterField(
            model_name='boaspraticas',
            name='segmento',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='wb.segmento'),
        ),
        migrations.DeleteModel(
            name='ReferenciaPessoal',
        ),
    ]
