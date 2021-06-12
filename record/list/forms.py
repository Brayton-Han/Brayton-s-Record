from django import forms 

class PreorderForm(forms.Form):
    amount = forms.IntegerField(required=True)

class OrderForm(forms.Form):
    status = forms.CharField(required=False)
    name = forms.CharField(required=False)
    cd = forms.BooleanField(required=False)

class TimeForm(forms.Form):
    start = forms.DateField(required=False)
    end = forms.DateField(required=False)