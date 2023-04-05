from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Empresa(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)
    empresa = models.CharField(max_length=200)
    cargo = models.CharField(max_length=200)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return 'Empresa: ' + str(self.empresa)

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'


class Questionario(models.Model):
    identificador = models.CharField(max_length=5)
    titulo_pergunta = models.CharField(max_length=250)
    pergunta = models.CharField(max_length=200)
    comentario = models.CharField(max_length=400)
    TIPOS = [("VA","ValorAtingido"),("VM","ValorMeta")]
    tipo = models.CharField(max_length=20, choices=TIPOS, default="VA")

    def __str__(self):
        if self.tipo == 'VM':
            return str(self.identificador) + ' - Valor Meta'
        return str(self.identificador) + ' - Valor Atingido'

    class Meta:
        verbose_name = 'Questionario'
        verbose_name_plural = 'Questionarios'


class Resposta(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    questao = models.ForeignKey(Questionario, on_delete=models.CASCADE)
    resposta = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return str(self.empresa) + ' - ' + str(self.questao)

    class Meta:
        verbose_name = 'Resposta'
        verbose_name_plural = 'Respostas'

class ValorReferencia(models.Model):
    questao = models.ForeignKey(Questionario, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=20, decimal_places=10)

    def __str__(self):
        return 'Valor de referencia - ' + str(self.questao)

    class Meta:
        verbose_name = 'ValorReferencia'
        verbose_name_plural = 'Valores de Referencia'

class Segmento(models.Model):
    segmento = models.CharField(max_length=200)

    def __str__(self):
        return self.segmento

    class Meta:
        verbose_name = 'Segmento'
        verbose_name_plural = 'Segmentos'

class EstrategiaCircular(models.Model):
    estrategiacircular = models.CharField(max_length=200)

    def __str__(self):
        return self.estrategiacircular

    class Meta:
        verbose_name = 'EstrategiaCircular'
        verbose_name_plural = 'Estrategias Circulares'

class BoasPraticas(models.Model):
    questao = models.ForeignKey(Questionario, on_delete=models.CASCADE,blank=True,null=True,default=None)
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    imagem = models.ImageField(upload_to ='uploads/',blank=True,null=True,default=None)
    empresa = models.CharField(max_length=200,blank=True,null=True,default=None)
    segmento = models.ForeignKey(Segmento, on_delete=models.CASCADE,blank=True,null=True,default=None)
    estrategiacircular = models.ForeignKey(EstrategiaCircular, on_delete=models.CASCADE,blank=True,null=True,default=None)
    boapratica = models.CharField(max_length=400,blank=True,null=True,default=None)
    fonte = models.CharField(max_length=200,blank=True,null=True,default=None)
    acesso = models.CharField(max_length=400,blank=True,null=True,default=None)

    def __str__(self):
        return str(self.titulo)

    class Meta:
        verbose_name = 'BoasPraticas'
        verbose_name_plural = 'Boas Praticas'