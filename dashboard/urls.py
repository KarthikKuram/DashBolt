from django.urls import path
from dashboard import views

urlpatterns = [
    path('redirect-settings/',views.Tally_Details_Redirect.as_view(), name='redirect_settings'),
    path('tally-settings/',views.Tally_Details_List.as_view(), name='tally_settings'),
    path('create-settings/',views.Tally_Details_CreateView.as_view(), name='create_tally_settings'),
    path('update-settings/<int:pk>/',views.Tally_Details_UpdateView.as_view(), name='update_tally_settings'),
    path('delete-settings/<int:pk>/',views.Tally_Details_DeleteView.as_view(), name='delete_tally_settings'),
    
]
