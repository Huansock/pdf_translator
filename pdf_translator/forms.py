from django import forms
from .models import Translator

class TranslatorForm(forms.ModelForm):
    
    class Meta:
        model = Translator
        fields = ('src_lang', 'dst_lang', 'pdf', "api_key" )
        labels = {
            'src_lang': 'Source Language',
            'dst_lang': 'Destination Language',
            'pdf': 'PDF',
            'api_key': 'open ai api_key'
        }
     
