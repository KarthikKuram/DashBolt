from django.views.generic import CreateView,UpdateView,RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import Tally_Details_Form
from .models import Tally_Detail
from django.urls import reverse_lazy, reverse


class Tally_Details_Redirect(LoginRequiredMixin,RedirectView):
    def get_redirect_url(self):
        if Tally_Detail.objects.filter(organization=self.request.user.organization).exists():
            return reverse('update_tally_settings')
        else:
            return reverse('create_tally_settings')
        
class Tally_Details_CreateView(LoginRequiredMixin,CreateView):
    form_class = Tally_Details_Form
    template_name = 'dashboard/tally_settings.html'
    success_message = 'Tally Settings Created'
    success_url = reverse_lazy('dashboard')
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.organization = self.request.user.organization
        obj.save()
        return super(Tally_Details_CreateView, self).form_valid(form)
    
class Tally_Details_UpdateView(LoginRequiredMixin,UpdateView):
    model = Tally_Detail
    form_class = Tally_Details_Form
    template_name = 'dashboard/tally_edit_settings.html'
    success_message = 'Tally Settings Updated'
    success_url = reverse_lazy('dashboard')
    
    def get_object(self,querset=None):
        tally_settings = self.model.objects.get(organization=self.request.user.organization)
        return tally_settings