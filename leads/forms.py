from django import forms

from .models import Lead


class BaseStyledModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            css_class = 'form-select' if isinstance(field.widget, forms.Select) else 'form-control'
            existing = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'{existing} {css_class}'.strip()


class LeadForm(BaseStyledModelForm):
    class Meta:
        model = Lead
        fields = ['full_name', 'phone', 'email', 'company', 'source', 'budget', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
        }


class LeadStatusForm(BaseStyledModelForm):
    class Meta:
        model = Lead
        fields = ['status']
