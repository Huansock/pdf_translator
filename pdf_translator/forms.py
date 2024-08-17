from django import forms
from .models import Translator

class TranslatorForm(forms.ModelForm):
    
    class Meta:
        model = Translator
        fields = ('src_lang', 'dst_lang', 'pdf','pdf_name', 'model_name')
        labels = {
            'src_lang': 'Source Language',
            'dst_lang': 'Destination Language',
            'pdf': 'PDF',
            'pdf_name': 'PDF Name',
            'model_name':'AI model name'
        }
     
