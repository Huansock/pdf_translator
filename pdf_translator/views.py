from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Translator
from .forms import TranslatorForm


def index(request):
	if request.method == "POST":
		form = TranslatorForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect("/pdf_translator/success/")
		print(form.errors)
	else:
		form = TranslatorForm()
	return render(request, "index.html", {"form": form})

def success(request):
	translators = Translator.objects.all()
	context = {
		"translators" : translators,
	}
	return render(request, "success.html" , context)