from django.forms import (Form, ModelForm, CharField, TextInput, PasswordInput, FloatField, NumberInput, ModelChoiceField, Select,
                      		DateTimeField, DateTimeInput)
from django.contrib.auth.models import User
from .models import Vehicle, Route, VehicleAssignment, Trip


class LoginForm(Form):
	username = CharField(min_length=1, max_length=50, widget=TextInput(attrs={
		'class': 'form-control',
		'placeholder': 'Enter the username'
	}))
	password = CharField(min_length=1, widget=PasswordInput(attrs={
		'class': 'form-control',
		'placeholder': 'Enter the password'
	}))


class RouteForm(ModelForm):
	class Meta:
		model = Route
		fields = ['start_point', 'end_point', 'distance']
		widgets = {
			'start_point': TextInput(attrs={
				'class': 'form-control',
				'placeholder': 'Enter the start point'
			}),
			'end_point': TextInput(attrs={
				'class': 'form-control',
				'placeholder': 'Enter the end point'
			}),
			'distance': NumberInput(attrs={
				'class': 'form-control'
			})
		}

class VehicleForm(ModelForm):
	class Meta:
		model = Vehicle
		fields = ['registration_code', 'model', 'fuel_usage']
		widgets = {
			'registration_code': TextInput(attrs={
				'class': 'form-control',
				'placeholder': 'Enter the registration code'
			}),
			'model': TextInput(attrs={
				'class': 'form-control',
				'placeholder': 'Enter the model'
			}),
			'fuel_usage': NumberInput(attrs={
				'class': 'form-control'
			})
		}

class VehicleAssignmentForm(ModelForm):
	class Meta:
		model = VehicleAssignment
		fields = ['vehicle']
		widgets = {
			'vehicle': Select(attrs={
				'class': 'form-control'
			})
		}

class TripForm(ModelForm):
	class Meta:
		model = Trip
		fields = ['route', 'assigned_vehicle', 'fuel_usage', 'start_time', 'end_time']
		widgets = {
			'route': Select(attrs={
				'class': 'form-control'
			}),
			'assigned_vehicle': Select(attrs={
				'class': 'form-control'
			}),
			'fuel_usage': NumberInput(attrs={
				'class': 'form-control'
			}),
			'start_time': DateTimeInput(attrs={
				'class': 'form-control',
				'type': 'datetime-local'
			}),
			'end_time': DateTimeInput(attrs={
				'class': 'form-control',
				'type': 'datetime-local'
			})
		}