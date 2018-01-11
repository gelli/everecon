from django import forms

from api.models import SolarSystem


def system_from_name(from_name):
    return SolarSystem.objects.filter(solar_system_name__iexact=from_name)


class NavigationForm(forms.Form):
    from_name = forms.CharField(widget=forms.TextInput(attrs={'id': 'from_name', 'placeholder': 'From'}))
    to_name = forms.CharField(widget=forms.TextInput(attrs={'id': 'to_name', 'placeholder': 'To'}))
    from_system = None
    to_system = None

    def clean(self):
        cleaned_data = super().clean()
        from_name = cleaned_data.get("from_name")
        to_name = cleaned_data.get("to_name")

        if self.is_valid():

            try:
                self.from_system = SolarSystem.objects.get(solar_system_name__iexact=from_name)
            except SolarSystem.DoesNotExist:
                self.add_error('from_name', 'System does not exist')

            try:
                self.to_system = SolarSystem.objects.get(solar_system_name__iexact=to_name)
            except SolarSystem.DoesNotExist:
                self.add_error('to_name', 'System does not exist')
