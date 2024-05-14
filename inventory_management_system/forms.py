from django import forms
from django.forms import ModelForm, DateInput
from inventory.models import *


class CustomDateInput(DateInput):
    input_type = 'date'


class AddForm(ModelForm):
    class Meta:
        model = Item
        fields = ['received_quantity']


class StockOutForm(ModelForm):
    class Meta:
        model = Sale
        fields = ['quantity', 'issued_to']


class MedicineForm(forms.ModelForm):
    valid_from = forms.DateField(label="Manufacture Date", widget=CustomDateInput(attrs={"class": "form-control"}))
    valid_to = forms.DateField(label="Expiry Date", widget=CustomDateInput(attrs={"class": "form-control"}))

    class Meta:
        model = Medicine
        fields = '__all__'
        exclude = ['reorder_level', 'receive_quantity']


class ReceiveMedicineForm(ModelForm):
    valid_to = forms.DateField(label="Expiry Date", widget=DateInput(attrs={"class": "form-control"}))

    class Meta:
        model = Medicine
        fields = '__all__'
        exclude = ['category', 'drug_name', 'valid_from', 'dispense_quantity', 'reorder_level', 'date_from', 'date_to',
                   'quantity', 'manufacture']


class ReorderLevelForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['reorder_level']
        
        
# class DispenseForm(ModelForm):
#     class Meta:
#         model = Dispense
#         fields = ['dispense_quantity', 'issued_to']


class LeaveForm(forms.ModelForm):
    class Meta:
        model = StaffLeave
        fields = ['leave_type', 'from_date', 'to_date', 'reason']
        
        
class LoginForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
        
        
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['user_type', 'profile_pic', 'first_name', 'last_name', 'email', 'username', 'password']