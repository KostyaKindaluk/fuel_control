from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .models import get_type, Driver, Route, Vehicle, VehicleAssignment, Trip
from .forms import LoginForm, RouteForm, VehicleForm, VehicleAssignmentForm, TripForm


def home(request):
	return render(request, 'home.html', {'type': get_type(request.user)})

def login(request):
	user_type = get_type(request.user)

	if request.method == 'GET':
		form = LoginForm()
		return render(request, "login.html", {'form': form, 'type': user_type})
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = auth.authenticate(request, username=username, password=password)
			
			if user is None:
				return render(request, "login.html",
					{'errors': ['Credentials are wrong'], 'form': form}
				)

			auth.login(request, user)
			return redirect('home')
		else:
			return render(request, "login.html",
				{'errors': ['Form is not valid'], 'form': form, 'type': user_type}
			)

@login_required
def logout(request):
	request.session.flush()
	return redirect('../')

@login_required
def routes(request):
	if get_type(request.user) != 'manager' and get_type(request.user) != 'driver':
		return redirect('home')
	return render(request, 'routes.html', {'type': get_type(request.user), 'routes': Route.objects.all()})

@login_required
def route_create(request):
	if get_type(request.user) != 'manager':
		return redirect('home')
  
	if request.method == 'GET':
		form = RouteForm()
		return render(request, 'route_form.html', {'form': form, 'type': get_type(request.user)})
	if request.method == 'POST':
		form = RouteForm(request.POST)
		if form.is_valid():
			form.save(commit=True)
			return redirect('routes')
		else:
			return render(request, "route_form.html",
				{'errors': ['Form is not valid'], 'form': form, 'type': get_type(request.user)}
			)

@login_required
def route_edit(request, route_id):
	if get_type(request.user) != 'manager':
		return redirect('home')
	
	route = get_object_or_404(Route, id=route_id)
	
	if request.method == 'GET':
		form = RouteForm(instance=route)
		return render(request, 'route_form.html', {'form': form, 'type': get_type(request.user)})
	if request.method == 'POST':
		form = RouteForm(request.POST, instance=route)
		if form.is_valid():
			form.save()
			return redirect('routes')
		else:
			return render(request, "route_form.html",
				{'errors': ['Form is not valid'], 'form': form, 'type': get_type(request.user)}
			)

@login_required
def route_delete(request, route_id):
	if get_type(request.user) != 'manager':
		return redirect('home')
  
	route = get_object_or_404(Route, id=route_id)

	if request.method == 'GET':
		return render(request, 'route_delete.html', {'type': get_type(request.user)})
	if request.method == 'POST':
		route.delete()
		return redirect('routes')

@login_required
def vehicles(request):
	if get_type(request.user) != 'manager':
		return redirect('home')
	return render(request, 'vehicles.html', {'type': get_type(request.user), 'vehicles': Vehicle.objects.all()})

@login_required
def vehicle_create(request):
	if get_type(request.user) != 'manager':
		return redirect('home')

	if request.method == 'GET':
		form = VehicleForm()
		return render(request, 'vehicle_form.html', {'form': form, 'type': get_type(request.user)})
	if request.method == 'POST':
		form = VehicleForm(request.POST)
		if form.is_valid():
			form.save(commit=True)
			return redirect('vehicles')
		else:
			return render(request, "vehicle_form.html",
				{'errors': ['Form is not valid'], 'form': form, 'type': get_type(request.user)}
			)

@login_required
def vehicle_edit(request, vehicle_id):
	if get_type(request.user) != 'manager':
		return redirect('home')
	
	vehicle = get_object_or_404(Vehicle, id=vehicle_id)
	
	if request.method == 'GET':
		form = VehicleForm(instance=vehicle)
		return render(request, 'vehicle_form.html', {'form': form, 'type': get_type(request.user)})
	if request.method == 'POST':
		form = VehicleForm(request.POST, instance=vehicle)
		if form.is_valid():
			form.save()
			return redirect('vehicles')
		else:
			return render(request, "vehicle_form.html",
				{'errors': ['Form is not valid'], 'form': form, 'type': get_type(request.user)}
			)

@login_required
def vehicle_delete(request, vehicle_id):
	if get_type(request.user) != 'manager':
		return redirect('home')
	
	vehicle = get_object_or_404(Vehicle, id=vehicle_id)

	if request.method == 'GET':
		return render(request, 'vehicle_delete.html', {'type': get_type(request.user)})
	if request.method == 'POST':
		vehicle.delete()
		return redirect('vehicles')


@login_required
def drivers(request):
	if get_type(request.user) != 'manager':
		return redirect('home')
	return render(request, 'drivers.html', {
		'type': get_type(request.user),
		'drivers': Driver.objects.all()
	})

@login_required
def driver(request, driver_id):
	if get_type(request.user) != 'manager' and get_type(request.user) != 'driver':
		return redirect('home')
	if get_type(request.user) == 'driver' and request.user.driver.id != driver_id:
		return redirect('home')
	
	driver = get_object_or_404(Driver, id=driver_id)
	vehicle_assignments = VehicleAssignment.objects.filter(driver=driver)
	trips = Trip.objects.filter(driver=driver)
	
	return render(request, 'driver.html', {
		'type': get_type(request.user),
		'driver': driver,
		'vehicle_assignments': vehicle_assignments,
		'trips': trips
	})


@login_required
def driver_assignVehicle(request, driver_id):
	if get_type(request.user) != 'manager':
		return redirect('home')

	driver = get_object_or_404(Driver, id=driver_id)

	if request.method == 'GET':
		form = VehicleAssignmentForm()
		return render(request, 'driver_assignVehicle.html', {'form': form, 'type': get_type(request.user), 'driver_id': driver_id})
	if request.method == 'POST':
		form = VehicleAssignmentForm(request.POST)
		if form.is_valid():
			vehicle_assignment = form.save(commit=False)
			vehicle_assignment.driver = driver
			vehicle_assignment.save()
			return redirect('driver', driver_id=driver_id)
		else:
			return render(request, "driver_assignVehicle.html",
				{'errors': ['Form is not valid'], 'form': form, 'type': get_type(request.user), 'driver_id': driver_id}
			)

@login_required
def driver_unassignVehicle(request, driver_id, assignment_id):
	if get_type(request.user) != 'manager':
		return redirect('home')
	
	assignment = get_object_or_404(VehicleAssignment, id=assignment_id, driver_id=driver_id)

	if request.method == 'GET':
		return render(request, 'driver_unassignVehicle.html', {'type': get_type(request.user), 'driver_id': driver_id})
	if request.method == 'POST':
		assignment.delete()
		return redirect('driver', driver_id=driver_id)


@login_required
def driver_trip_create(request, driver_id):
	if get_type(request.user) != 'driver':
		return redirect('home')
	if request.user.driver.id != driver_id:
		return redirect('home')
	
	driver = get_object_or_404(Driver, id=driver_id)
  
	if request.method == 'GET':
		form = TripForm()
		return render(request, 'driver_trip_form.html', {'form': form, 'type': get_type(request.user), 'driver_id': driver_id})
	if request.method == 'POST':
		form = TripForm(request.POST)
		if form.is_valid():
			trip = form.save(commit=False)
			trip.driver = driver
			trip.expected_fuel_usage = trip.route.distance * trip.assigned_vehicle.vehicle.fuel_usage / 100
			trip.save()
			return redirect('driver', driver_id=driver_id)
		else:
			return render(request, "driver_trip_form.html",
				{'errors': ['Form is not valid'], 'form': form, 'type': get_type(request.user), 'driver_id': driver_id}
			)

@login_required
def driver_trip_edit(request, driver_id, trip_id):
	if get_type(request.user) != 'driver':
		return redirect('driver', driver_id=driver_id)
	if request.user.driver.id != driver_id:
		return redirect('driver', driver_id=driver_id)
	
	trip = get_object_or_404(Trip, id=trip_id, driver_id=driver_id)
	
	if request.method == 'GET':
		form = TripForm(instance=trip)
		return render(request, 'driver_trip_form.html', {'form': form, 'type': get_type(request.user), 'driver_id': driver_id})
	if request.method == 'POST':
		form = TripForm(request.POST, instance=trip)
		if form.is_valid():
			trip = form.save(commit=False)
			trip.expected_fuel_usage = trip.route.distance * trip.assigned_vehicle.vehicle.fuel_usage / 100
			trip.save()
			return redirect('driver', driver_id=driver_id)
		else:
			return render(request, "driver_trip_form.html",
				{'errors': ['Form is not valid'], 'form': form, 'type': get_type(request.user), 'driver_id': driver_id}
			)

@login_required
def driver_trip_delete(request, driver_id, trip_id):
	if get_type(request.user) != 'driver':
		return redirect('driver', driver_id=driver_id)
	if request.user.driver.id != driver_id:
		return redirect('driver', driver_id=driver_id)

	trip = get_object_or_404(Trip, id=trip_id, driver_id=driver_id)

	if request.method == 'GET':
		return render(request, 'driver_trip_delete.html', {'type': get_type(request.user)})
	if request.method == 'POST':
		trip.delete()
		return redirect('driver', driver_id=driver_id)