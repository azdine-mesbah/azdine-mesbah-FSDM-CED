from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, ModelFormMixin, UpdateView
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404

from .models import Departement, Enseignant, Laboratoire, Sujet, FormationDoctorale, FormationComplementaire
from .forms import DepartmentCreateForm, LaboratoireCreateForm, SujetCreateForm, FormationDoctoraleCreateForm, FormationComplementaireCreateForm


# Departements CRUD
class DepartementListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'Administration.view_departement'
    template_name = 'departement_index.html'
    paginate_by = 10
    context_object_name = 'departements'

    def get_queryset(self):
        queryset = Departement.objects.all()
        if self.request.GET.get('search'):
            search = self.request.GET.get('search')
            queryset = Departement.objects.filter(Q(intitule__icontains=search)|Q(description__icontains=search))
            if queryset:
                messages.success(self.request, f"{len(queryset)} resultats trouvé")
            else:
                messages.error(self.request, "Aucune resultats trouvé")
        return queryset

class DepartementCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'Administration.add_departement'
    template_name = 'ajax_departement_create.html'
    form_class = DepartmentCreateForm

    def get_success_url(self):
        return reverse('departement-list')

    def form_valid(self, form):
        if self.request.is_ajax():
            super().form_valid(form)
            return JsonResponse({"redirect":self.get_success_url()}, status=302)
        return super().form_valid(form)

class DepartementDetailView(LoginRequiredMixin,PermissionRequiredMixin, ModelFormMixin, DetailView):
    permission_required = 'Administration.view_departement'
    model = Departement
    fields = '__all__'
    template_name = 'departement_detail.html'

class DepartementEditView(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    permission_required = 'Administration.edit_departement'
    model = Departement
    fields = '__all__'
    
    def get_success_url(self):
        return reverse('departement-detail', kwargs={'pk':self.object.id})

class DepartementDeleteView(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
    permission_required = 'Administration.delete_departement'
    model = Departement

    def get_success_url(self):
        return reverse('departement-list')


# Enseignant CRUD

class EnseignantListView(LoginRequiredMixin,PermissionRequiredMixin, ListView):
    permission_required = 'Administration.view_Enseignant'
    template_name = 'enseignant_index.html'
    paginate_by = 10
    context_object_name = 'enseignants'
    
    def get_queryset(self):
        queryset = Enseignant.objects.all()
        if self.request.GET.get('search'):
            search = self.request.GET.get('search')
            queryset = Enseignant.objects.filter(
                Q(nom__icontains=search)|
                Q(prenom__icontains=search)|
                Q(etablissement__intitule__icontains=search)|
                Q(etablissement__ville__icontains=search))
            if queryset:
                messages.success(self.request, f"{len(queryset)} resultats trouvé")
            else:
                messages.error(self.request, "Aucune resultats trouvé")
        return queryset

class EnseignantCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'Administration.add_enseignant'
    model = Enseignant
    template_name = 'ajax_enseignant_create.html'
    fields = "__all__"

    def get_success_url(self):
        return reverse('enseignant-list', kwargs={})

    def form_valid(self, form):
        if self.request.is_ajax():
            super().form_valid(form)
            return JsonResponse({"redirect":self.get_success_url()}, status=302)
        return super().form_valid(form)

class EnseignantDetailView(LoginRequiredMixin,PermissionRequiredMixin, ModelFormMixin, DetailView):
    permission_required = 'Administration.view_enseignant'
    model = Enseignant
    fields = "__all__"
    template_name = 'enseignant_detail.html'
    
class EnseignantEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'Administration.edit_enseignant'
    model = Enseignant
    fields = '__all__'
    template_name = 'enseignant_detail.html'
    
    def get_success_url(self):
        return reverse('enseignant-detail', kwargs={'pk':self.object.id})

class EnseignantDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'Administration.delete_enseignant'
    model = Enseignant
    
    def get_success_url(self):
        return reverse('enseignant-list')


# Laboratoire CRUD
class LaboratoireCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'Administration.add_laboratoire'
    template_name = 'ajax_laboratoire_create.html'
    form_class = LaboratoireCreateForm

    def get_initial(self):
        departement = get_object_or_404(Departement, pk=self.kwargs.get('departement_id'))
        return {"departement":departement}
    
    def get_success_url(self):
        return reverse('departement-detail', kwargs={'pk':self.kwargs.get('departement_id')})
    
    def form_valid(self, form):
        if self.request.is_ajax():
            super().form_valid(form)
            return JsonResponse({"redirect":self.get_success_url()}, status=302)
        return super().form_valid(form)

class LaboratoireEditView(LaboratoireCreateView, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'Administration.edit_laboratoire'
    template_name = 'ajax_laboratoire_detail.html'
    model = Laboratoire

class LaboratoireDeleteView(LaboratoireEditView, LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'Administration.delete_laboratoire'
    model = Laboratoire


# Sujet CRUD
class SujetCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'Administration.add_sujet'
    template_name = 'ajax_sujet_create.html'
    form_class = SujetCreateForm
    model = Sujet

    def get_initial(self):
        enseignant = get_object_or_404(Enseignant, pk=self.kwargs.get('enseignant_id'))
        return {"directeur":enseignant, 'laboratoire':enseignant.get_current_laboratoire()}
    
    def get_success_url(self):
        return reverse('enseignant-detail', kwargs={'pk':self.kwargs.get('enseignant_id')})
    
    def form_valid(self, form):
        if self.request.is_ajax():
            super().form_valid(form)
            return JsonResponse({"redirect":self.get_success_url()}, status=302)
        return super().form_valid(form)

class SujetEditView(SujetCreateView, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'Administration.edit_sujet'
    template_name = 'ajax_sujet_detail.html'
    
class SujetDeleteView(SujetEditView, LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'Administration.delete_sujet'


# Formation doctorale CRUD
class FormationDoctoraleListView(LoginRequiredMixin,PermissionRequiredMixin, ListView):
    permission_required = 'Administration.view_formation_doctorale'
    template_name = 'formation_index.html'
    paginate_by = 10
    context_object_name = 'formations'

    def get_queryset(self):
        queryset = FormationDoctorale.objects.all()
        if self.request.GET.get('search'):
            search = self.request.GET.get('search')
            queryset = FormationDoctorale.objects.filter(
                Q(intitule__icontains=search)|
                Q(acronyme__icontains=search)|
                Q(description__icontains=search)|
                Q(co_ordonateur__nom__icontains=search)|
                Q(co_ordonateur__prenom__icontains=search))
            if queryset:
                messages.success(self.request, f"{len(queryset)} resultats trouvé")
            else:
                messages.error(self.request, "Aucune resultats trouvé")
        return queryset

class FormationDoctoraleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'Administration.add_formation_doctorale'
    template_name = 'ajax_formation_d_create.html'
    model = FormationDoctorale
    form_class = FormationDoctoraleCreateForm

    def get_success_url(self):
        return reverse('formation-list')
    
    def form_valid(self, form):
        if self.request.is_ajax():
            super().form_valid(form)
            return JsonResponse({"redirect":self.get_success_url()}, status=302)
        return super().form_valid(form)

class FormationDoctoraleDetailView(LoginRequiredMixin, PermissionRequiredMixin, ModelFormMixin, DetailView):
    permission_required = 'Administration.view_formation_doctorale'
    model = FormationDoctorale
    template_name = 'formation_d_detail.html'
    context_object_name = 'formation'
    form_class = FormationDoctoraleCreateForm

class FormationDoctoraleEditView(FormationDoctoraleCreateView, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'Administration.edit_formation_doctorale'
    def get_success_url(self):
        return reverse('formation-detail', kwargs={'pk':self.object.id})

class FormationDoctoraleDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'Administration.delete_formation_doctorale'
    model = FormationDoctorale
    def get_success_url(self):
        return reverse('formation-list')


# Formation complementaire CRUD
class FormationComplementaireCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'Administration.add_formation_complementaire'
    template_name = 'ajax_formation_c_create.html'
    form_class = FormationComplementaireCreateForm
    model = FormationComplementaire
    context_object_name = 'fc'
    
    def get_initial(self):
        formation = get_object_or_404(FormationDoctorale, pk=self.kwargs.get('formation_id'))
        print('*'*50,formation, '*'*50, sep='\n')
        return {"formation":formation}
    
    def get_success_url(self):
        return reverse('formation-detail', kwargs={'pk':self.kwargs.get('formation_id')})
    
    def form_valid(self, form):
        if self.request.is_ajax():
            super().form_valid(form)
            return JsonResponse({"redirect":self.get_success_url()}, status=302)
        return super().form_valid(form)

class FormationComplementaireEditView(FormationComplementaireCreateView, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'Administration.edit_formation_complementaire'
    template_name = 'ajax_formation_c_detail.html'

class FormationComplementaireDeleteView(FormationComplementaireEditView, LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'Administration.delete_formation_complementaire'

