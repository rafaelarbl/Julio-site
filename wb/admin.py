from django.contrib import admin
from .models import Empresa, Questionario, Resposta, ValorReferencia, BoasPraticas,Segmento,EstrategiaCircular

admin.site.register(Empresa)
admin.site.register(Questionario)
admin.site.register(Resposta)
admin.site.register(ValorReferencia)
admin.site.register(BoasPraticas)
admin.site.register(Segmento)
admin.site.register(EstrategiaCircular)