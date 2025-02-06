from fatalities.models import Comment, CustomerEmail
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)

class EmailForm(forms.ModelForm):
    class Meta:
        model = CustomerEmail
        fields = ('email',)
        widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'ben@roadway.report'}),
        }
