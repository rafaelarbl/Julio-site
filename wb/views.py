from django.shortcuts import render,redirect
from .forms import EmpresaForm, QuestionarioForm,RespostaForm, SignUpForm, LoginForm, PasswordResetForm
from .models import Questionario, Empresa, Resposta, ValorReferencia, BoasPraticas
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
	boaspraticas = BoasPraticas.objects.all()

	lista = []
	diction = {}
	grafico_valores = []
	grafico_referencias = []
	grafico_metas = []
	grafico_valores2 = []
	for index,resposta1 in enumerate(respostas):
		lista=[]
		for resposta2 in respostas:
			if resposta1.questao != resposta2.questao and resposta1.questao.identificador == resposta2.questao.identificador: #questoes diferentes com o mesmo identificador
				if resposta1.questao.tipo == 'VM' and resposta2.questao.tipo == 'VA': #resposta1 tem a meta e resposta2 tem o valor atingido
					if resposta1.questao.identificador == "IW1" or resposta1.questao.identificador == "IE1":
						valor_atingido = (1 - ((resposta2.resposta - resposta1.resposta) / resposta1.resposta)) * 100
						meta_empresa = 100
						lista.append(valor_atingido)
						grafico_valores.append(valor_atingido)
						grafico_metas.append(meta_empresa)
					else:
						meta_empresa = resposta1.resposta
						valor_atingido = resposta2.resposta
						lista.append(valor_atingido)
						grafico_metas.append(meta_empresa)
						grafico_valores.append(valor_atingido)
					for vr in valorreferencia:
						if vr.questao == resposta2.questao:
							if vr.questao.identificador == "IW1" or vr.questao.identificador == "IE1":
								referencia = (1 - ((resposta2.resposta - vr.valor) / vr.valor)) * 100
								lista.append(referencia)
								grafico_referencias.append(100)
								grafico_valores2.append(referencia)
							else:
								referencia = vr.valor * 100
								lista.append(referencia)
								grafico_referencias.append(referencia)
								grafico_valores2.append(resposta2.resposta)
					diction[resposta1.questao.identificador] = lista

	oce_meta = []
	oce_referencia = []
	for key, value in diction.items():
		if key == 'IW1' or key == 'IE1':
			a = value[0]
			if value[0] > 100:
				a = 100
			if value[0] < 0:
				a = 0
			oce_meta.append(a)

			a = value[1]
			if value[1] > 100:
				a = 100
			if value[1] < 0:
				a = 0
			oce_referencia.append(a)
		else:
			a = value[0]
			if value[0] > 100:
				a = 100
			if value[0] < 0:
				a = 0
			oce_meta.append(a)

			a = value[0]
			if value[0] > 100:
				a = 100
			if value[0] < 0:
				a = 0
			oce_referencia.append(a)

	media_meta = 0
	print(oce_meta)
	if len(oce_meta) > 0:
		media_meta = sum(oce_meta)/len(oce_meta)
	media_referencia = 0
	print(oce_referencia)
	if len(oce_referencia) > 0:
		media_referencia = sum(oce_referencia)/len(oce_referencia)
	return render(request, 'wb/respostas.html', {'grafico_valores2':grafico_valores2, 'valorreferencia':valorreferencia,'grafico_metas':grafico_metas,'grafico_valores':grafico_valores,'grafico_referencias':grafico_referencias,'diction':diction,'empresa':empresa,'questoes':questoes,'lista':lista,'oce_meta':media_meta,'oce_referencia':media_referencia,'boaspraticas':boaspraticas})


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