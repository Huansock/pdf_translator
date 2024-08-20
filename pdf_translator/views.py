from django.http import FileResponse
from django.shortcuts import render
from .models import Translator
from .forms import TranslatorForm
from logic.ai_translator import ai_translator
from django.conf import settings
import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings

def index(request):
	if request.method == "POST":
		form = TranslatorForm(request.POST, request.FILES)
		

		if form.is_valid():
			pdf_file = form.cleaned_data['pdf']
			if pdf_file.name.endswith('.pdf'):
				# FileSystemStorage를 사용하여 MEDIA_ROOT에 파일 저장
				fs = FileSystemStorage(location=settings.PDFS_ROOT)
				filename = fs.save(pdf_file.name, pdf_file)
			pdf_name = str(form.cleaned_data["pdf"])[:-4]
			src_lang = form.cleaned_data["src_lang"]
			dst_lang = form.cleaned_data["dst_lang"]
			api_key = form.cleaned_data["api_key"]
			ai_translator.translate(pdf_name=pdf_name, src_lang=src_lang, dst_lang=dst_lang , api_key=api_key)
			file_path = os.path.join(settings.MEDIA_ROOT, 'markdowns', f"{pdf_name}_{src_lang}_to_{dst_lang}.md")
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