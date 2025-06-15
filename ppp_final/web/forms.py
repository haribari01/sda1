from django import forms
from .models import Evaluation

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['order', 'name', 'topic', 'report', 'rating', 'score', 'best', 'suspected_gpt']
        widgets = {
            'order': forms.NumberInput(attrs={'readonly': 'readonly', 'style': 'width: 60px;'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 140px;'}),
            'topic': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 270px;'}),
            'report': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 200px;'}),
            'rating': forms.NumberInput(attrs={'min': 0, 'max': 5, 'style': 'width: 70px;'}),
            'score': forms.TextInput(attrs={'readonly': 'readonly', 'style': 'width: 60px; background:#eee;'}),
        }
