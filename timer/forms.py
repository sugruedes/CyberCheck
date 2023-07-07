from django import forms

from .models import Dweet, Profile


class RaceForm(forms.Form):
    swimmers = forms.ModelMultipleChoiceField(
        widget=forms.widgets.SelectMultiple(
            attrs={
                "class": "textarea is-success is-medium",
            }
        ),
        label="",
        queryset=None)


    def __init__(self, *args, **kwargs):
        race_id = kwargs.pop('race_id', None) # Correctly obtains slug from url
        super().__init__(*args, **kwargs)
        self.fields['swimmers'].queryset = Profile.objects.all().exclude(swims_in=race_id)

class DweetForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Dweet something...",
                "class": "textarea is-success is-medium",
            }
        ),
        label="",
    )

    class Meta:
        model = Dweet
        exclude = ("user",)
