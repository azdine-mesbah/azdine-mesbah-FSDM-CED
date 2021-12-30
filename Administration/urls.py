from django.urls import path
from . import views

urlpatterns = [
    path('departements/', views.DepartementListView.as_view(), name="departement-list"),
    path('departements/create', views.DepartementCreateView.as_view(), name="departement-create"),
    path('departements/detail/<int:pk>', views.DepartementDetailView.as_view(), name="departement-detail"),
    path('departements/edit/<int:pk>', views.DepartementEditView.as_view(), name="departement-edit"),
    path('departements/delete/<int:pk>', views.DepartementDeleteView.as_view(), name="departement-delete"),

    path('departments/<int:departement_id>/laboratoires/create/', views.LaboratoireCreateView.as_view(), name="laboratoire-create"),
    path('departments/<int:departement_id>/laboratoires/detail/<int:pk>', views.LaboratoireEditView.as_view(), name="laboratoire-detail"),
    path('departments/<int:departement_id>/laboratoires/edit/<int:pk>', views.LaboratoireEditView.as_view(), name="laboratoire-edit"),
    path('departments/<int:departement_id>/laboratoires/delete/<int:pk>', views.LaboratoireDeleteView.as_view(), name="laboratoire-delete"),

    path('enseignants/', views.EnseignantListView.as_view(), name="enseignant-list"),
    path('enseignants/create', views.EnseignantCreateView.as_view(), name="enseignant-create"),
    path('enseignants/detail/<int:pk>', views.EnseignantDetailView.as_view(), name="enseignant-detail"),
    path('enseignants/edit/<int:pk>', views.EnseignantEditView.as_view(), name="enseignant-edit"),
    path('enseignants/delete/<int:pk>', views.EnseignantDeleteView.as_view(), name="enseignant-delete"),

    path('enseignants/<int:enseignant_id>/sujets/create/', views.SujetCreateView.as_view(), name="sujet-create"),
    path('enseignants/<int:enseignant_id>/sujets/detail/<int:pk>', views.SujetEditView.as_view(), name="sujet-detail"),
    path('enseignants/<int:enseignant_id>/sujets/edit/<int:pk>', views.SujetEditView.as_view(), name="sujet-edit"),
    path('enseignants/<int:enseignant_id>/sujets/delete/<int:pk>', views.SujetDeleteView.as_view(), name="sujet-delete"),
]