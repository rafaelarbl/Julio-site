from django import forms

from .models import Empresa, Questionario, Resposta

class SignUpForm(forms.Form):
    usuario = forms.CharField(max_length=30)
    email = forms.EmailField()
    senha = forms.CharField(widget=forms.PasswordInput)


class LoginForm(forms.Form):
    usuario = forms.CharField(max_length=30)
    senha = forms.CharField(widget=forms.PasswordInput)

class PasswordResetForm(forms.Form):
    email = forms.EmailField()

class EmpresaForm(forms.ModelForm):

    class Meta:
        model = Empresa
        fields = ('nome', 'email','empresa','cargo')

class QuestionarioForm(forms.ModelForm):

    class Meta:
        model = Questionario
        fields = ('identificador', 'titulo_pergunta','pergunta','comentario')

class RespostaForm(forms.ModelForm):

    class Meta:
        model = Resposta
        fields = ('empresa','questao','resposta',)
