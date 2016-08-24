from django import forms


class AddProductForm(forms.Form):
    name = forms.CharField(max_length=100)
    description = forms.TextInput()
    category = forms.IntegerField()
    image = forms.ImageField()
    size = forms.CharField(max_length=10)
    colour = forms.CharField(max_length=40)
    price = forms.FloatField()
    quantity = forms.IntegerField()
