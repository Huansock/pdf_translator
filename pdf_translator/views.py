from django.http import FileResponse
from django.shortcuts import render
from .models import Translator
from .forms import TranslatorForm
from logic.ai_translator import ai_translator
from django.conf import settings
import os

def index(request):
	if request.method == "POST":
		form = TranslatorForm(request.POST, request.FILES)
		

		if form.is_valid():
			pdf_name = str(form.cleaned_data["pdf"])[:-4]
			src_lang = form.cleaned_data["src_lang"]
			dst_lang = form.cleaned_data["dst_lang"]
			api_key = form.cleaned_data["api_key"]
			ai_translator.translate(pdf_name=pdf_name, src_lang=src_lang, dst_lang=dst_lang)
			file_path = os.path.join(settings.MEDIA_ROOT, 'markdowns', f"{pdf_name}_{src_lang}_to_{dst_lang}.pdf")
			return FileResponse(open(file_path, 'rb'))
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