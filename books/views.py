from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.http import Http404
from .models import Book, Section, Subsection
from .serializers import BookSerializer, SectionSerializer, SubsectionSerializer
from .permissions import IsAuthorOrCollaborator
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

User = get_user_model()

class BookListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @method_decorator(cache_page(60*60*2, key_prefix='book_list_view_cache_'))
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data['author'] = request.user.id  # Set the author field to the authenticated user's ID
        serializer = BookSerializer(data=data)

        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrCollaborator]

    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        book = self.get_object(pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def put(self, request, pk):
        book = self.get_object(pk)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        book = self.get_object(pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SectionListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        book_id = request.data.get('book')
        book = Book.objects.get(pk=book_id)

        # Check if the user is the author of the book
        if request.user != book.author:
            return Response("Only the author can create sections for this book.", status=status.HTTP_403_FORBIDDEN)

        serializer = SectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SectionDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrCollaborator]

    def get_object(self, pk):
        try:
            return Section.objects.get(pk=pk)
        except Section.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        section = self.get_object(pk)
        serializer = SectionSerializer(section)
        return Response(serializer.data)

    def put(self, request, pk):
        section = self.get_object(pk)

        # Check if the user is the author or a collaborator of the book
        if request.user != section.book.author and request.user not in section.book.collaborators.all():
            return Response("Only the author and collaborators can edit this section.", status=status.HTTP_403_FORBIDDEN)

        serializer = SectionSerializer(section, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        section = self.get_object(pk)
        
        if request.user != section.book.author:
            return Response("Only the author can delete this section.", status=status.HTTP_403_FORBIDDEN)

        section.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SubsectionListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        section_id = request.data.get('section')
        section = Section.objects.get(pk=section_id)
        book = section.book

        # Check if the user is the author of the book
        if request.user != book.author:
            return Response("Only the author can create subsections for this book.", status=status.HTTP_403_FORBIDDEN)

        serializer = SubsectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubsectionDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrCollaborator]

    def get_object(self, pk):
        try:
            return Subsection.objects.get(pk=pk)
        except Subsection.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        subsection = self.get_object(pk)
        serializer = SubsectionSerializer(subsection)
        return Response(serializer.data)

    def put(self, request, pk):
        subsection = self.get_object(pk)

        # Check if the user is the author or a collaborator of the book
        if request.user != subsection.section.book.author and request.user not in subsection.section.book.collaborators.all():
            return Response("Only the author and collaborators can edit this subsection.", status=status.HTTP_403_FORBIDDEN)

        serializer = SubsectionSerializer(subsection, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        subsection = self.get_object(pk)
        if request.user != subsection.section.book.author:
            return Response("Only the author can delete this section.", status=status.HTTP_403_FORBIDDEN)

        subsection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class AddCollaboratorView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, book_id, user_id):
        # Ensure the user making the request is the book's author
        book = Book.objects.get(pk=book_id)
        if request.user != book.author:
            return Response("You do not have permission to add a collaborator.", status=status.HTTP_403_FORBIDDEN)

        # Add the specified user as a collaborator
        user = User.objects.get(pk=user_id)
        book.collaborators.add(user)
        return Response("Collaborator added.", status=status.HTTP_200_OK)

class RemoveCollaboratorView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, book_id, user_id):
        # Ensure the user making the request is the book's author
        book = Book.objects.get(pk=book_id)
        if request.user != book.author:
            return Response("You do not have permission to remove a collaborator.", status=status.HTTP_403_FORBIDDEN)

        # Remove the specified user as a collaborator
        user = User.objects.get(pk=user_id)
        book.collaborators.remove(user)
        return Response("Collaborator removed.", status=status.HTTP_200_OK)
