from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse
from django.http.response import JsonResponse
from django.views.generic.edit import CreateView, DeleteView, ModelFormMixin, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404

from .models import Doctorant, Cursus, Inscription, Retrait
from .forms import DoctorantCreateForm, CursusCreateForm, RetraitCreateForm, InscriptionCreateForm



# Doctorant CRUD
class DoctorantListView(LoginRequiredMixin,PermissionRequiredMixin, ListView):
    permission_required = 'Doctorant.view_doctorant'
    template_name = 'doctorant_index.html'
    paginate_by = 10
    context_object_name = 'doctorants'
    
    def get_queryset(self):
        queryset = Doctorant.objects.all()
        if self.request.GET.get('search'):
            search = self.request.GET.get('search')
            queryset = Doctorant.objects.filter(Q(cin__icontains=search)|Q(cne__icontains=search)|Q(nom__icontains=search)|Q(prenom__icontains=search))
            if queryset:
                messages.success(self.request, f"{len(queryset)} resultats trouvé")
            else:
                messages.error(self.request, "Aucune resultats trouvé")
        return queryset

class DoctorantCreateView(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    permission_required = 'Doctorant.add_doctorant'
    template_name = 'doctorant_create.html'
    form_class = DoctorantCreateForm
    
    def get_success_url(self):
        return reverse('doctorant-detail', kwargs={'pk':self.object.id})

class DoctorantDetailView(LoginRequiredMixin,PermissionRequiredMixin, ModelFormMixin, DetailView):
    permission_required = 'Doctorant.view_doctorant'
    model = Doctorant
    template_name = 'doctorant_detail.html'
    form_class = DoctorantCreateForm
    
class DoctorantEditView(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    permission_required = 'Doctorant.edit_doctorant'
    model = Doctorant
    template_name = 'doctorant_detail.html'
    fields = '__all__'
    
    def get_success_url(self):
        return reverse('doctorant-detail', kwargs={'pk':self.object.id})

class DoctorantDeletView(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
    permission_required = 'Doctorant.delete_doctorant'
    model = Doctorant

    def get_success_url(self):
        return reverse('doctorant-list')


# Cursus CRUD
class CursusCreateView(LoginRequiredMixin, CreateView):
    template_name = 'ajax_cursus_create.html'
    form_class = CursusCreateForm

    def get_initial(self):
        doctorant = get_object_or_404(Doctorant, pk=self.kwargs.get('doctorant_id'))
        return {"doctorant":doctorant}
    
    def get_success_url(self):
        return reverse('doctorant-detail', kwargs={'pk':self.kwargs.get('doctorant_id')})
    
    def form_valid(self, form):
        if self.request.is_ajax():
            super().form_valid(form)
            return JsonResponse({"redirect":self.get_success_url()}, status=302)
        return super().form_valid(form)

class CursusEditView(LoginRequiredMixin, UpdateView):
    model = Cursus
    template_name = 'ajax_cursus_detail.html'
    form_class = CursusCreateForm

    def get_initial(self):
        doctorant = get_object_or_404(Doctorant, pk=self.kwargs.get('doctorant_id'))
        return {"doctorant":doctorant}

    def get_success_url(self):
        return reverse('doctorant-detail', kwargs={'pk':self.kwargs.get('doctorant_id')})

class CursusDeleteView(LoginRequiredMixin, DeleteView):
    model = Cursus

    def get_initial(self):
        doctorant = get_object_or_404(Doctorant, pk=self.kwargs.get('doctorant_id'))
        return {"doctorant":doctorant}

    def get_success_url(self):
        return reverse('doctorant-detail', kwargs={'pk':self.kwargs.get('doctorant_id')})


# Retrait CRUD
class RetraitCreateView(LoginRequiredMixin, CreateView):
    form_class = RetraitCreateForm
    template_name = 'ajax_retrait_create.html'

    def get_initial(self):
        doctorant = get_object_or_404(Doctorant, pk=self.kwargs.get('doctorant_id'))
        return {"doctorant":doctorant}
    
    def get_success_url(self):
        return reverse('doctorant-detail', kwargs={'pk':self.kwargs.get('doctorant_id')})

class RetraitEditView(LoginRequiredMixin, UpdateView):
    model = Retrait
    template_name = 'ajax_retrait_detail.html'
    form_class = RetraitCreateForm

    def get_initial(self):
        doctorant = get_object_or_404(Doctorant, pk=self.kwargs.get('doctorant_id'))
        return {"doctorant":doctorant}

    def get_success_url(self):
        return reverse('doctorant-detail', kwargs={'pk':self.kwargs.get('doctorant_id')})

class RetraitDeleteView(LoginRequiredMixin, DeleteView):
    model = Retrait
    
    def get_initial(self):
        doctorant = get_object_or_404(Doctorant, pk=self.kwargs.get('doctorant_id'))
        return {"doctorant":doctorant}

    def get_success_url(self):
        return reverse('doctorant-detail', kwargs={'pk':self.kwargs.get('doctorant_id')})


# Inscription CRUD
class InscriptionCreateView(LoginRequiredMixin, CreateView):
    form_class = InscriptionCreateForm

    def get_initial(self):
        self.template_name = 'ajax_inscription_create.html'
        doctorant = get_object_or_404(Doctorant, pk=self.kwargs.get('doctorant_id'))
        return {"doctorant":doctorant}
    
    def get_success_url(self):
        return reverse('doctorant-detail', kwargs={'pk':self.kwargs.get('doctorant_id')})

class InscriptionEditView(LoginRequiredMixin, UpdateView):
    model = Inscription
    form_class = InscriptionCreateForm

    def get_initial(self):
        self.template_name = 'ajax_inscription_detail.html'
        doctorant = get_object_or_404(Doctorant, pk=self.kwargs.get('doctorant_id'))
        return {"doctorant":doctorant}

    def get_success_url(self):
        return reverse('doctorant-detail', kwargs={'pk':self.kwargs.get('doctorant_id')})

class InscriptionDeleteView(LoginRequiredMixin, DeleteView):
    model = Inscription
    def get_initial(self):
        doctorant = get_object_or_404(Doctorant, pk=self.kwargs.get('doctorant_id'))
        return {"doctorant":doctorant}

    def get_success_url(self):
        return reverse('doctorant-detail', kwargs={'pk':self.kwargs.get('doctorant_id')})