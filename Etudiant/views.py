from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse
from django.http.response import JsonResponse
from django.views.generic.edit import CreateView, DeleteView, ModelFormMixin, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views import View
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.shortcuts import render


from .models import Doctorant, Cursus, Inscription, Retrait, Publication, Soutenance, SoutenanceMembers
from .forms import DoctorantCreateForm, CursusCreateForm, RetraitCreateForm, InscriptionCreateForm, PublicationCreateForm, SoutenanceCreateForm, SoutenanceMemberCreateForm



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
    permission_required = 'Doctorant.change_doctorant'
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
    model = Cursus

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

class CursusEditView(CursusCreateView, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'Doctorant.change_cursus'
    template_name = 'ajax_cursus_detail.html'

class CursusDeleteView(CursusEditView, LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'Doctorant.delete_cursus'


# Retrait CRUD
class RetraitCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'Doctorant.add_retrait'
    model = Retrait
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

class RetraitEditView(RetraitCreateView, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'Doctorant.change_retrait'
    template_name = 'ajax_retrait_detail.html'

class RetraitDeleteView(RetraitEditView, LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'Doctorant.delete_retrait'


# Inscription CRUD
class InscriptionCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'Doctorant.add_inscription'
    form_class = InscriptionCreateForm
    template_name = 'ajax_inscription_create.html'
    model = Inscription

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
    permission_required = 'Doctorant.change_inscription'
    template_name = 'ajax_inscription_detail.html'

class InscriptionDeleteView(InscriptionEditView, LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'Doctorant.delete_inscription'


# Publication CRUD
class PublicationCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'Doctorant.add_publication'
    template_name = 'ajax_publication_create.html'
    form_class = PublicationCreateForm
    model = Publication

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
    permission_required = 'Doctorant.change_publication'
    template_name = 'ajax_publication_detail.html'

class PublicationDeleteView(PublicationEditView, LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'Doctorant.delete_publication'


# Soutenence CRUD
class SoutenanceCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'Doctorant.add_soutenance'
    template_name = 'ajax_soutenance_create.html'
    form_class = SoutenanceCreateForm
    model = Soutenance

    def get_initial(self):
        doctorant = get_object_or_404(Doctorant, pk=self.kwargs.get('doctorant_id'))
        return {"doctorant":doctorant}
    
    def get_success_url(self):
        return reverse('soutenance-detail', kwargs={'doctorant_id':self.kwargs.get('doctorant_id')})

    def form_valid(self, form):
        if self.request.is_ajax():
            super().form_valid(form)
            return JsonResponse({"redirect":self.get_success_url()}, status=302)
        return super().form_valid(form)

class SoutenanceDetailView(SoutenanceCreateView, LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'Doctorant.view_soutenance'
    template_name = 'soutenance_detail.html'

    def get_object(self):
        doctorant = get_object_or_404(Doctorant, pk=self.kwargs.get('doctorant_id'))
        soutenance = get_object_or_404(Soutenance, pk=doctorant.soutenance.pk)
        return soutenance
    
class SoutenanceEditView(SoutenanceDetailView, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'Doctorant.change_soutenance'

class SoutenanceDeleteView(SoutenanceDetailView, LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'Doctorant.delete_soutenance'

    def get_success_url(self):
        return reverse('doctorant-detail', kwargs={'pk':self.kwargs.get('doctorant_id')})
        
    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({"redirect":self.get_success_url()}, status=302)


# Soutenance Members CRUD
class MemberCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'Doctorant.add_soutenancemembers'
    template_name = 'ajax_soutenance_member_create.html'
    form_class = SoutenanceMemberCreateForm
    model = SoutenanceMembers
    context_object_name = 'soutenence_member'

    def get_initial(self):
        return {
            "doctorant":get_object_or_404(Doctorant, pk=self.kwargs.get('doctorant_id')),
            "type": self.kwargs.get('type'),
            "pk":self.kwargs.get('pk')
            }

    def get_success_url(self):
        return reverse('soutenance-detail', kwargs={'doctorant_id':self.kwargs.get('doctorant_id')})

    def form_valid(self, form):
        if self.request.is_ajax():
            super().form_valid(form)
            return JsonResponse({"redirect":self.get_success_url()}, status=302)
        return super().form_valid(form)

class MemberEditView(MemberCreateView, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'Doctorant.change_soutenancemembers'
    template_name = 'ajax_soutenance_member_detail.html'

class MemberDeleteView(MemberEditView, LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'Doctorant.delete_soutenancemembers'

class SoutenancePreviewView(LoginRequiredMixin, PermissionRequiredMixin, ModelFormMixin, View):
    permission_required = 'Doctorant.preview_soutenance'
    model = Soutenance
    template_name = 'soutenance/previews/%s.html'

    def get_object(self):
        doctorant = get_object_or_404(Doctorant, pk=self.kwargs.get('doctorant_id'))
        soutenance = get_object_or_404(Soutenance, pk=doctorant.soutenance.pk)
        return soutenance

    def get(self, request, *args, **kwargs):
        data = {
            "template":request.GET.get('template'),
            "receivers":request.GET.getlist('receivers')
        }
        return render(request, self.template_name % data['template'], context={"soutenance":self.get_object()})