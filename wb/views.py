from django.shortcuts import render,redirect
from .forms import EmpresaForm, QuestionarioForm,RespostaForm, SignUpForm, LoginForm, PasswordResetForm
from .models import Questionario, Empresa, Resposta, ValorReferencia,TargetGrafico, BoasPraticas
from django.contrib import messages
from django.forms import modelformset_factory
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.response import TemplateResponse
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import json
from django.shortcuts import get_object_or_404

def index(request):
	try:
		empresa = Empresa.objects.filter(usuario=request.user).last()
	except TypeError:
		empresa = None
	return render(request, 'wb/index.html',{'empresa':empresa})

def nova_empresa(request):
	empresa = Empresa.objects.filter(usuario=request.user).last()
	if request.method == "POST":
		if empresa:
			form = EmpresaForm(request.POST, instance=empresa)
		else:
			form = EmpresaForm(request.POST)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.usuario = request.user
			obj.save()
			messages.success(request, "Empresa salva com sucesso.")
			return redirect('questionario')
	else:
		if empresa:
			form = EmpresaForm(instance=empresa)
		else:
			form = EmpresaForm()
		print(empresa) # comentário
		return render(request, 'wb/nova_empresa.html', {'form': form,'empresa':empresa})

def questionario(request):
	questoes = Questionario.objects.all()
	try:
		empresa = Empresa.objects.filter(usuario=request.user).last()
	except TypeError:
		empresa = None
	respostas = Resposta.objects.filter(empresa=empresa)

	initial = []
	for index,questao in enumerate(questoes):
		d = {'empresa': empresa}
		d['questao'] = questao
		for resposta in respostas:
			if resposta.questao == questao:
				d['resposta'] = resposta.resposta
		initial.append(d)

	RespostaFormSet = modelformset_factory(Resposta, form=RespostaForm,fields=('empresa', 'questao','resposta'),extra=len(questoes))
	formset = RespostaFormSet(queryset=Resposta.objects.none(),initial=initial)

	if request.method == "POST":
		formset = RespostaFormSet(request.POST)
		if all(form.is_valid() for form in formset):
			for index,f in enumerate(formset):
				if f.is_valid():
					try:
						d = Resposta.objects.get(id=respostas[index].id)
						d.resposta = f.cleaned_data.get('resposta')
						d.save()
					except IndexError as e:
						form = f.save(commit=False)
						f.empresa = empresa
						f.save()
			messages.success(request, "Questionario salvo com sucesso.")
			return redirect('respostas')
		else:
			print('AAAAAAAAAAA')
			print(formset.errors)
			messages.error(request, "Por favor preencha todas as informações antes de enviar.")
			return redirect('questionario')


	return render(request, 'wb/questionario.html', {'empresa':empresa,'formset': formset,'questoes':questoes})


def respostas(request):
	questoes = Questionario.objects.all()
	valorreferencia = ValorReferencia.objects.all()
	try:
		empresa = Empresa.objects.filter(usuario=request.user).last()
	except TypeError:
		empresa = None
	respostas = Resposta.objects.filter(empresa=empresa)
	targets = TargetGrafico.objects.all()
	boaspraticas = BoasPraticas.objects.all()

	lista = []
	for resposta in respostas:
		for valor in valorreferencia:
			if resposta.questao == valor.questao:
				if resposta.questao.id == 1 or resposta.questao.id == 2:
					res = 100 - (100 * ((resposta.resposta - valor.valor ) / valor.valor ))
					print (resposta.resposta)
					print(valor.valor)
				else:
					res = resposta.resposta
				lista.append(res)
	media = 0
	if len(lista) > 0:
		media = sum(lista)/len(lista)

	return render(request, 'wb/respostas.html', {'empresa':empresa,'questoes':questoes,'lista':lista,'media':media,'targets':targets,'boaspraticas':boaspraticas})


def cadastrar(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            usuario = form.cleaned_data['usuario']
            password = form.cleaned_data['senha']
            try:
                user = User.objects.create_user(username=usuario,email=email, password=password)
            except IntegrityError as e:
                messages.error(request, "Este usuario ja existe.")
                form = SignUpForm()
                return render(request, 'wb/cadastrar.html', {'form': form, 'error': e})
            login(request, user)
            messages.success(request, "Conta criada com sucesso.")
            return redirect('nova_empresa')
    else:
        form = SignUpForm()
    return render(request, 'wb/cadastrar.html', {'form': form})

def loginview(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['usuario']
            password = form.cleaned_data['senha']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login efetuado com sucesso.")
                return redirect('nova_empresa')
    else:
        form = LoginForm()
    return render(request, 'wb/login.html', {'form': form})

def esqueceuasenha(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = get_user_model().objects.get(email=email)
            except ObjectDoesNotExist as e:
                messages.error(request, "Nenhum usuário cadastrado com este email")
                form = PasswordResetForm()
                return render(request, 'wb/esqueceuasenha.html', {'form': form})
            if user is not None:
                token = default_token_generator.make_token(user)
                messages.success(request, "Troque a senha atraves do email")
                return redirect('loginview')
    else:
        form = PasswordResetForm()
    return render(request, 'wb/esqueceuasenha.html', {'form': form})

def sair(request):
	logout(request)
	return redirect('loginview')

def boaspraticas(request):
	boaspraticas = BoasPraticas.objects.all()
	try:
		empresa = Empresa.objects.filter(usuario=request.user).last()
	except TypeError:
		empresa = None

	return render(request, 'wb/boaspraticas.html', {'boaspraticas':boaspraticas,'empresa':empresa})

def boaspraticasdetalhada(request, pk):
  boapratica = get_object_or_404(BoasPraticas, id=pk)
  try:
    empresa = Empresa.objects.filter(usuario=request.user).last()
  except TypeError:
  	empresa = None
  return render (request, 'wb/boapraticadetalhada.html', {'boapratica': boapratica,'empresa':empresa})