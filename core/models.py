from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def get_type(user):
	if not user.is_authenticated:
		return 'no auth'

	if hasattr(user, 'driver'):
		return 'driver'
	elif hasattr(user, 'manager'):
		return 'manager'
	return 'admin'


class Driver(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver')
	full_name = models.CharField(max_length=50)

	def clean(self):
		super().clean()
		if not self.full_name.strip():
			raise ValidationError({'full_Name': 'Full name can\'t be empty'})
	def __str__(self):
		return f"{self.full_name}"

class Manager(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='manager')
	full_name = models.CharField(max_length=50)

	def clean(self):
		super().clean()
		if not self.full_name.strip():
			raise ValidationError({'full_Name': 'Full name can\'t be empty'})
	def __str__(self):
		return f"{self.full_name}"


class Route(models.Model):
	start_point = models.CharField(max_length=50)
	end_point = models.CharField(max_length=50)
	distance = models.FloatField()

	def clean(self):
		super().clean()
		if not self.start_point.strip():
			raise ValidationError({'start_point': 'Start point can\'t be empty'})
		if not self.end_point.strip():
			raise ValidationError({'end_point': 'End point can\'t be empty'})
		if (self.distance < 0):
			raise ValidationError({'distance': 'Distance can\'t be negative'})
	def __str__(self):
		return f"From '{self.start_point}' to '{self.end_point}', distance: {self.distance} KM"

class Vehicle(models.Model):
	registration_code = models.CharField(max_length=10)
	model = models.CharField(max_length=50)
	fuel_usage = models.FloatField()

	def clean(self):
		super().clean()
		if not self.registration_code.strip():
			raise ValidationError({'registration_code': 'Registration code can\'t be empty'})
		if not self.model.strip():
			raise ValidationError({'model': 'Model can\'t be empty'})
		if (self.fuel_usage < 0):
			raise ValidationError({'fuel_usage': 'Fuel usage can\'t be negative'})
	def __str__(self):
		return f"{self.model} ({self.registration_code}), fuel usage: {self.fuel_usage} L/KM"

class VehicleAssignment(models.Model):
	driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_query_name='vehicle_assignments')
	vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_query_name='vehicle_assignments')
	def __str__(self):
		return f"{self.vehicle} of {self.driver}"

class Trip(models.Model):
	driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
	route = models.ForeignKey(Route, on_delete=models.CASCADE)
	assigned_vehicle = models.ForeignKey(VehicleAssignment, on_delete=models.CASCADE)

	fuel_usage = models.FloatField()
	expected_fuel_usage = models.FloatField()

	start_time = models.DateTimeField()
	end_time = models.DateTimeField()

	def clean(self):
		super().clean()
		if (self.fuel_usage < 0):
			raise ValidationError({'fuel_usage': 'Fuel usage can\'t be negative'})
	def __str__(self):
		return f"Driver: {self.driver}, route: {self.route}, vehicle: {self.assigned_vehicle.vehicle}, fuel usage: {self.fuel_usage} L"