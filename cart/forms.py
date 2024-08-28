from django import forms


class AddToCartRoomForm(forms.Form):
    inplace = forms.BooleanField(required=False, widget=forms.HiddenInput)


class BookingForm(forms.Form):
    arrival_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    departure_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    adults = forms.IntegerField(min_value=1, max_value=10, initial=2)
    children = forms.IntegerField(min_value=0, max_value=10, initial=0)
    infants = forms.IntegerField(min_value=0, max_value=10, initial=0)