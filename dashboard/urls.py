from django.urls import path
from dashboard import views
from django.contrib.auth.decorators import user_passes_test
from .models import Tally_Detail

urlpatterns = [
    # path('redirect-settings/',views.Tally_Details_Redirect.as_view(), name='redirect_settings'),
    path('tally-settings/',
         user_passes_test(lambda u: u.org_admin)(views.Tally_Details_List.as_view()), name='tally_settings'),
    path('create-settings/',views.Tally_Details_CreateView.as_view(), name='create_tally_settings'),
    path('update-settings/<int:pk>/',views.Tally_Details_UpdateView.as_view(), name='update_tally_settings'),
    path('delete-settings/<int:pk>/',views.Tally_Details_DeleteView.as_view(), name='delete_tally_settings'),
    path('valid_users/<int:pk>/',
         user_passes_test(lambda u: u.org_admin and Tally_Detail.objects.filter(organization = u.organization))(views.Tally_Valid_Users.as_view()), name='valid_users'),
    path('update-dashboard/', views.update_dashboard, name = 'update_dashboard'),
    
]
