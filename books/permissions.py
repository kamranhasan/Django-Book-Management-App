from rest_framework import permissions

class IsAuthorOrCollaborator(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        # Check if the user is the author or a collaborator of the book
        return request.user == obj.book.author or request.user in obj.book.collaborators.all()