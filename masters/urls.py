from django.urls import path
from . import views

app_name = 'masters'

urlpatterns = [
    # Manufacturer
    path('manufacturers/', views.ManufacturerListView.as_view(), name='manufacturer_list'),
    path('manufacturers/add/', views.ManufacturerCreateView.as_view(), name='manufacturer_add'),
    path('manufacturers/edit/<int:pk>/', views.ManufacturerUpdateView.as_view(), name='manufacturer_edit'),
    path('manufacturers/delete/<int:pk>/', views.ManufacturerDeleteView.as_view(), name='manufacturer_delete'),

    # Buying House
    path('buying-houses/', views.BuyingHouseListView.as_view(), name='buying_house_list'),
    path('buying-houses/add/', views.BuyingHouseCreateView.as_view(), name='buying_house_add'),
    path('buying-houses/edit/<int:pk>/', views.BuyingHouseUpdateView.as_view(), name='buying_house_edit'),
    path('buying-houses/delete/<int:pk>/', views.BuyingHouseDeleteView.as_view(), name='buying_house_delete'),

    # Agent
    path('agents/', views.AgentListView.as_view(), name='agent_list'),
    path('agents/add/', views.AgentCreateView.as_view(), name='agent_add'),
    path('agents/edit/<int:pk>/', views.AgentUpdateView.as_view(), name='agent_edit'),
    path('agents/delete/<int:pk>/', views.AgentDeleteView.as_view(), name='agent_delete'),

        # Fabric
    path('fabrics/', views.FabricListView.as_view(), name='fabric_list'),
    path('fabrics/add/', views.FabricCreateView.as_view(), name='fabric_add'),
    path('fabrics/edit/<int:pk>/', views.FabricUpdateView.as_view(), name='fabric_edit'),
    path('fabrics/delete/<int:pk>/', views.FabricDeleteView.as_view(), name='fabric_delete'),
]