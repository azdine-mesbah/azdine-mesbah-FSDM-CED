from django.urls import path
from . import views

urlpatterns = [
    path('', views.DoctorantListView.as_view(), name="doctorant-list"),
    path('create/', views.DoctorantCreateView.as_view(), name="doctorant-create"),
    path('detail/<int:pk>/', views.DoctorantDetailView.as_view(), name="doctorant-detail"),
    path('edit/<int:pk>/', views.DoctorantEditView.as_view(), name="doctorant-edit"),
    path('delete/<int:pk>/', views.DoctorantDeletView.as_view(), name="doctorant-delete"),

    path('<int:doctorant_id>/cursus/create/', views.CursusCreateView.as_view(), name="cursus-create"),
    path('<int:doctorant_id>/cursus/detail/<int:pk>/', views.CursusEditView.as_view(), name="cursus-detail"),
    path('<int:doctorant_id>/cursus/edit/<int:pk>/', views.CursusEditView.as_view(), name="cursus-edit"),
    path('<int:doctorant_id>/cursus/delete/<int:pk>/', views.CursusDeleteView.as_view(), name="cursus-delete"),

    path('<int:doctorant_id>/retraits/create/', views.RetraitCreateView.as_view(), name="retrait-create"),
    path('<int:doctorant_id>/retraits/detail/<int:pk>/', views.RetraitEditView.as_view(), name="retrait-detail"),
    path('<int:doctorant_id>/retraits/edit/<int:pk>/', views.RetraitEditView.as_view(), name="retrait-edit"),
    path('<int:doctorant_id>/retraits/delete/<int:pk>/', views.RetraitDeleteView.as_view(), name="retrait-delete"),
    
    path('<int:doctorant_id>/inscription/create/', views.InscriptionCreateView.as_view(), name="inscription-create"),
    path('<int:doctorant_id>/inscription/detail/<int:pk>/', views.InscriptionEditView.as_view(), name="inscription-detail"),
    path('<int:doctorant_id>/inscription/edit/<int:pk>/', views.InscriptionEditView.as_view(), name="inscription-edit"),
    path('<int:doctorant_id>/inscription/delete/<int:pk>/', views.InscriptionDeleteView.as_view(), name="inscription-delete"),

    path('<int:doctorant_id>/publications/create/', views.PublicationCreateView.as_view(), name="publication-create"),
    path('<int:doctorant_id>/publications/detail/<int:pk>/', views.PublicationEditView.as_view(), name="publication-detail"),
    path('<int:doctorant_id>/publications/edit/<int:pk>/', views.PublicationEditView.as_view(), name="publication-edit"),
    path('<int:doctorant_id>/publications/delete/<int:pk>/', views.PublicationDeleteView.as_view(), name="publication-delete"),

    path('<int:doctorant_id>/soutenance/create/', views.SoutenanceCreateView.as_view(), name="soutenance-create"),
    path('<int:doctorant_id>/soutenance/detail/', views.SoutenanceDetailView.as_view(), name="soutenance-detail"),
    path('<int:doctorant_id>/soutenance/edit/', views.SoutenanceEditView.as_view(), name="soutenance-edit"),
    path('<int:doctorant_id>/soutenance/delete/', views.SoutenanceDeleteView.as_view(), name="soutenance-delete"),

    path('<int:doctorant_id>/soutenance/<type>/create', views.MemberCreateView.as_view(), name="member-create"),
    path('<int:doctorant_id>/soutenance/<type>/detail/<int:pk>', views.MemberEditView.as_view(), name="member-detail"),
    path('<int:doctorant_id>/soutenance/<type>/edit/<int:pk>', views.MemberEditView.as_view(), name="member-edit"),
    path('<int:doctorant_id>/soutenance/<type>/delete/<int:pk>', views.MemberDeleteView.as_view(), name="member-delete"),

    path('<int:doctorant_id>/soutenance/preview/', views.SoutenancePreviewView.as_view(), name="soutenance-preview"),
    path('<int:doctorant_id>/soutenance/pdf/', views.SoutenancePDFView.as_view(), name="soutenance-pdf"),
]