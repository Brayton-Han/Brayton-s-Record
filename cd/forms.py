from collections import defaultdict
from django import forms 

class QuerycdForm(forms.Form):
    name = forms.CharField(max_length=128, required=False)
    artist = forms.CharField(max_length=128, required=False)
    explicit = forms.BooleanField(required=False)
    seal_off = forms.BooleanField(required=False)

class QueryvinylForm(forms.Form):
    name = forms.CharField(max_length=128, required=False)
    artist = forms.CharField(max_length=128, required=False)
    second_hand = forms.BooleanField(required=False)

class EditcdForm(forms.Form):
    barcode = forms.CharField(max_length=13)
    name = forms.CharField(max_length=128)
    artist = forms.CharField(max_length=128, required=False)
    number = forms.IntegerField(required=False)
    genre = forms.CharField(max_length=128, required=False)
    produce_area = forms.CharField(max_length=128)
    price = forms.FloatField()
    cost = forms.FloatField()
    seal_off = forms.BooleanField(required=False)
    explicit = forms.BooleanField(required=False)

class EditvinylForm(forms.Form):
    barcode = forms.CharField(max_length=13)
    name = forms.CharField(max_length=128)
    artist = forms.CharField(max_length=128, required=False)
    number = forms.IntegerField(required=False)
    genre = forms.CharField(max_length=128, required=False)
    produce_area = forms.CharField(max_length=128)
    price = forms.FloatField()
    cost = forms.FloatField()
    second_hand = forms.BooleanField(required=False)