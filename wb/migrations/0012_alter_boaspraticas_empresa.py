# Generated by Django 4.1.4 on 2023-01-03 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wb', '0011_estrategiacircular_segmento_boaspraticas_acesso_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boaspraticas',
            name='empresa',
            field=models.CharField(default=None, max_length=200),
        ),
    ]