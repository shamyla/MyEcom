from django import forms
from django.forms import modelformset_factory
from .models import Variation


class VariationInventoryForm(forms.ModelForm):
    class Meta:
        model = Variation
        fields = [
            "title",
            "price",
            "sale_price",
            "inventory",
            'active',

        ]

VariationInventoryFormset = modelformset_factory(Variation, VariationInventoryForm, extra=0)