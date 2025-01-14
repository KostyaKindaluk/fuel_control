from django.urls import path
from . import views


urlpatterns = [
	path('', views.home, name='home'),
	path('login', views.login, name='login'),
  path('logout', views.logout, name='logout'),
  
  path('routes', views.routes, name='routes'),
  path('routes/create', views.route_create, name='route_create'),
  path('routes/<int:route_id>/edit', views.route_edit, name='route_edit'),
  path('routes/<int:route_id>/delete', views.route_delete, name='route_delete'),
  
  path('vehicles', views.vehicles, name='vehicles'),
  path('vehicles/create', views.vehicle_create, name='vehicle_create'),
  path('vehicles/<int:vehicle_id>/edit', views.vehicle_edit, name='vehicle_edit'),
  path('vehicles/<int:vehicle_id>/delete', views.vehicle_delete, name='vehicle_delete'),
  
  path('drivers', views.drivers, name='drivers'),
  path('drivers/<int:driver_id>', views.driver, name='driver'),
	path('drivers/<int:driver_id>/assignVehicle', views.driver_assignVehicle, name='driver_assignVehicle'),
  path('drivers/<int:driver_id>/unassignVehicle/<int:assignment_id>', views.driver_unassignVehicle, name='driver_unassignVehicle'),
  path('drivers/<int:driver_id>/trips/create', views.driver_trip_create, name='driver_trip_create'),
  path('drivers/<int:driver_id>/trips/<int:trip_id>/edit', views.driver_trip_edit, name='driver_trip_edit'),
  path('drivers/<int:driver_id>/trips/<int:trip_id>/delete', views.driver_trip_delete, name='driver_trip_delete'),
]