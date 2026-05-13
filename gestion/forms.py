from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Cliente, Empleado, Mesa, Plato, Orden, Factura


class IngresoForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'placeholder': 'Usuario', 'autocomplete': 'username'}
        )
        self.fields['password'].widget.attrs.update(
            {'placeholder': 'Contraseña', 'autocomplete': 'current-password'}
        )


class RegistroAdministradorForm(UserCreationForm):
    """Alta de usuario con rol único por ahora: administrador del restaurante (acceso a la app)."""

    email = forms.EmailField(required=True, label='Correo electrónico')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'placeholder': 'Usuario', 'autocomplete': 'username'}
        )
        self.fields['email'].widget.attrs.update(
            {'placeholder': 'correo@ejemplo.com', 'autocomplete': 'email'}
        )
        self.fields['password1'].widget.attrs.update({'autocomplete': 'new-password'})
        self.fields['password2'].widget.attrs.update({'autocomplete': 'new-password'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'


class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = '__all__'


class MesaForm(forms.ModelForm):
    class Meta:
        model = Mesa
        fields = '__all__'


class PlatoForm(forms.ModelForm):
    class Meta:
        model = Plato
        fields = '__all__'


class OrdenForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = '__all__'


class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = '__all__'