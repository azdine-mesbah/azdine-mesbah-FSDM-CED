from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse
from django.http.response import JsonResponse
from django.views.generic.edit import CreateView, DeleteView, ModelFormMixin, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404

from .models import Doctorant, Cursus, Inscription, Retrait, Publication
from .forms import DoctorantCreateForm, CursusCreateForm, RetraitCreateForm, InscriptionCreateForm, PublicationCreateForm



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
class CursusCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'Doctorant.add_cursus'
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

class CursusEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'Doctorant.edit_cursus'
    model = Cursus
    template_name = 'ajax_cursus_detail.html'
    form_class = CursusCreateForm

    def get_initial(self):
        doctorant = get_object_or_404(Doctorant, pk=self.kwargs.get('doctorant_id'))
        return {"doctorant":doctorant}

    def get_success_url(self):
        return reverse('doctorant-detail', kwargs={'pk':self.kwargs.get('doctorant_id')})

class CursusDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'Doctorant.delete_cursus'
    model = Cursus

    def get_initial(self):
        doctorant = get_object_or_404(Doctorant, pk=self.kwargs.get('doctorant_id'))
        return {"doctorant":doctorant}

    def get_success_url(self):
        return reverse('doctorant-detail', kwargs={'pk':self.kwargs.get('doctorant_id')})


# Retrait CRUD
class RetraitCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'Doctorant.add_retrait'
    form_class = RetraitCreateForm
    template_name = 'ajax_retrait_create.html'

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

class RetraitEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'Doctorant.edit_retrait'
    model = Retrait
    template_name = 'ajax_retrait_detail.html'
    form_class = RetraitCreateForm

    def get_initial(self):
        doctorant = get_object_or_404(Doctorant, pk=self.kwargs.get('doctorant_id'))
        return {"doctorant":doctorant}

    def get_success_url(self):
        return reverse('doctorant-detail', kwargs={'pk':self.kwargs.get('doctorant_id')})

class RetraitDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'Doctorant.delete_retrait'
    model = Retrait
    
    def get_initial(self):
        doctorant = get_object_or_404(Doctorant, pk=self.kwargs.get('doctorant_id'))
        return {"doctorant":doctorant}

    def get_success_url(self):
        return reverse('doctorant-detail', kwargs={'pk':self.kwargs.get('doctorant_id')})


# Inscription CRUD
class InscriptionCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'Doctorant.add_inscription'
    form_class = InscriptionCreateForm
    template_name = 'ajax_inscription_create.html'

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

class InscriptionEditView(InscriptionCreateView, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'Doctorant.edit_inscription'
    model = Inscription
    template_name = 'ajax_inscription_detail.html'

class InscriptionDeleteView(InscriptionEditView, LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'Doctorant.delete_inscription'


# Publication CRUD
class PublicationCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'Doctorant.add_publication'
    form_class = PublicationCreateForm
    template_name = 'ajax_publication_create.html'

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
    
class PublicationEditView(PublicationCreateView, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'Doctorant.edit_publication'
    model = Publication
    template_name = 'ajax_publication_detail.html'

class PublicationDeleteView(PublicationEditView, LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'Doctorant.delete_publication'