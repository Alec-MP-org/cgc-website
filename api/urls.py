from django.urls import path
from api import views

urlpatterns = [
    path('api/details/', views.FlightsheetDetails_create.as_view(), name="details_all"),
    path('api/details/<str:pk>/', views.FlightsheetDetails_edit.as_view(), name="details_select"),
    path('api/detailsdate/<str:pk>/', views.FlightsheetDetails_edit_many.as_view(), name="details_select_many"),
    path('api/headers/', views.FlightsheetHeader_create.as_view(), name="headers_all"),
    path('api/headers/<str:pk>/', views.FlightsheetHeader_edit.as_view(), name="headers_select"),
]