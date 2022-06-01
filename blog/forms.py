from django import forms
from django.core.exceptions import ValidationError

from .models  import News
import re
# https://djbook.ru/rel3.0/topics/forms/index.html

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = 'title', 'content', 'category' #'__all__'рекомендується прописати всі =[ 'title', 'content', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows':6}),
            'category': forms.Select(attrs={'class': 'form-control'})
        }

    # def clean_title(self):
    #     title = self.cleaned_data['title']
    #     if re.match(r'\d',title):
    #         raise ValidationError('назва статті не повинна починатися з цифри')