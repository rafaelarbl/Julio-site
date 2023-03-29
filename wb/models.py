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


class Questionario(models.Model):
    identificador = models.CharField(max_length=5)
    titulo_pergunta = models.CharField(max_length=250)
    pergunta = models.CharField(max_length=200)
    comentario = models.CharField(max_length=200)

    def __str__(self):
        return 'Questao '+ str(self.id)+' ('+str(self.identificador)+')'

class Resposta(models.Model):
	empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
	questao = models.ForeignKey(Questionario, on_delete=models.CASCADE)
	resposta = models.DecimalField(max_digits=20, decimal_places=10)

	def __str__(self):
		return str(self.empresa) + ' - ' + str(self.questao)

class ValorReferencia(models.Model):
	questao = models.ForeignKey(Questionario, on_delete=models.CASCADE)
	valor = models.DecimalField(max_digits=20, decimal_places=10)

	def __str__(self):
		return 'Valor de referencia - ' + str(self.questao)


class TargetGrafico(models.Model):
    questao = models.ForeignKey(Questionario, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=20, decimal_places=10)

    def __str__(self):
        return 'Target do grafico - ' + str(self.questao)

class Segmento(models.Model):
    segmento = models.CharField(max_length=200)

    def __str__(self):
        return self.segmento

class EstrategiaCircular(models.Model):
    estrategiacircular = models.CharField(max_length=200)

    def __str__(self):
        return self.estrategiacircular

class BoasPraticas(models.Model):
    questao = models.ForeignKey(Questionario, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    imagem = models.ImageField(upload_to ='uploads/',blank=True,null=True,default=None)
    empresa = models.CharField(max_length=200,blank=True,null=True,default=None)
    segmento = models.ForeignKey(Segmento, on_delete=models.CASCADE,blank=True,null=True)
    estrategiacircular = models.ForeignKey(EstrategiaCircular, on_delete=models.CASCADE,blank=True,null=True,default=None)
    boapratica = models.CharField(max_length=400,blank=True,null=True,default=None)
    fonte = models.CharField(max_length=200,blank=True,null=True,default=None)
    acesso = models.CharField(max_length=400,blank=True,null=True,default=None)

    def __str__(self):
        return str(self.titulo)