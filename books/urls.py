from django.urls import path
from . import views

urlpatterns = [
    # Book views
    path('books/', views.BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),

    # Section views
    path('sections/', views.SectionListCreateView.as_view(), name='section-list-create'),
    path('sections/<int:pk>/', views.SectionDetailView.as_view(), name='section-detail'),

    # Subsection views
    path('subsections/', views.SubsectionListCreateView.as_view(), name='subsection-list-create'),
    path('subsections/<int:pk>/', views.SubsectionDetailView.as_view(), name='subsection-detail'),
    
    # Add Collaborator
    path('books/<int:book_id>/add-collaborator/<int:user_id>/', views.AddCollaboratorView.as_view(), name='add-collaborator'),

    # Remove Collaborator
    path('books/<int:book_id>/remove-collaborator/<int:user_id>/', views.RemoveCollaboratorView.as_view(), name='remove-collaborator'),

]