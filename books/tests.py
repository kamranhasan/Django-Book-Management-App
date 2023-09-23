from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Book, Section, Subsection

class BookAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_author = User.objects.create_user(username='author', password='password123')
        self.user_collaborator = User.objects.create_user(username='collaborator', password='password123')
        self.user_regular = User.objects.create_user(username='regular', password='password123')
        self.book = Book.objects.create(title='Test Book', author=self.user_author)
        self.book.collaborators.add(self.user_collaborator)
        self.section = Section.objects.create(title='Test Section', book=self.book)
        self.subsection = Subsection.objects.create(title='Test Subsection', section=self.section)

    def test_create_book(self):
        self.client.force_authenticate(user=self.user_author)
        response = self.client.post('/api/books/', {'title': 'New Book'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_section_as_author(self):
        self.client.force_authenticate(user=self.user_author)
        response = self.client.post('/api/sections/', {'book': self.book.id, 'title': 'New Section'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_section_as_collaborator(self):
        self.client.force_authenticate(user=self.user_collaborator)
        response = self.client.post('/api/sections/', {'book': self.book.id, 'title': 'New Section'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_section_as_regular_user(self):
        self.client.force_authenticate(user=self.user_regular)
        response = self.client.post('/api/sections/', {'book': self.book.id, 'title': 'New Section'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_subsection_as_author(self):
        self.client.force_authenticate(user=self.user_author)
        response = self.client.post('/api/subsections/', {'section': self.section.id, 'title': 'New Subsection'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_subsection_as_collaborator(self):
        self.client.force_authenticate(user=self.user_collaborator)
        response = self.client.post('/api/subsections/', {'section': self.section.id, 'title': 'New Subsection'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_subsection_as_regular_user(self):
        self.client.force_authenticate(user=self.user_regular)
        response = self.client.post('/api/subsections/', {'section': self.section.id, 'title': 'New Subsection'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_edit_section_as_author(self):
        self.client.force_authenticate(user=self.user_author)
        response = self.client.put(f'/api/sections/{self.section.id}/', {'title': 'Updated Section'})
        if response.status_code != status.HTTP_200_OK:
            print(f"Response Content: {response.content}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_section_as_collaborator(self):
        self.client.force_authenticate(user=self.user_collaborator)
        response = self.client.put(f'/api/sections/{self.section.id}/', {'title': 'Updated Section'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_section_as_regular_user(self):
        self.client.force_authenticate(user=self.user_regular)
        response = self.client.put(f'/api/sections/{self.section.id}/', {'title': 'Updated Section'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_edit_subsection_as_author(self):
        self.client.force_authenticate(user=self.user_author)
        response = self.client.put(f'/api/subsections/{self.subsection.id}/', {'title': 'Updated Subsection'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_subsection_as_collaborator(self):
        self.client.force_authenticate(user=self.user_collaborator)
        response = self.client.put(f'/api/subsections/{self.subsection.id}/', {'title': 'Updated Subsection'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_subsection_as_regular_user(self):
        self.client.force_authenticate(user=self.user_regular)
        response = self.client.put(f'/api/subsections/{self.subsection.id}/', {'title': 'Updated Subsection'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_section_as_author(self):
        self.client.force_authenticate(user=self.user_author)
        response = self.client.delete(f'/api/sections/{self.section.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_section_as_collaborator(self):
        self.client.force_authenticate(user=self.user_collaborator)
        response = self.client.delete(f'/api/sections/{self.section.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_section_as_regular_user(self):
        self.client.force_authenticate(user=self.user_regular)
        response = self.client.delete(f'/api/sections/{self.section.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_subsection_as_author(self):
        self.client.force_authenticate(user=self.user_author)
        response = self.client.delete(f'/api/subsections/{self.subsection.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_subsection_as_collaborator(self):
        self.client.force_authenticate(user=self.user_collaborator)
        response = self.client.delete(f'/api/subsections/{self.subsection.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_subsection_as_regular_user(self):
        self.client.force_authenticate(user=self.user_regular)
        response = self.client.delete(f'/api/subsections/{self.subsection.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_collaborator(self):
        # Authenticate as the author
        self.client.force_authenticate(user=self.user_author)

        # Add the collaborator to the book
        response = self.client.post(f'/api/books/{self.book.id}/add-collaborator/{self.user_regular.id}/')

        # Check if the collaborator was added successfully
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the collaborator is in the book's collaborators list
        self.book.refresh_from_db()
        self.assertTrue(self.user_regular in self.book.collaborators.all())

    def test_remove_collaborator(self):
        # Authenticate as the author
        self.client.force_authenticate(user=self.user_author)

        # Remove the collaborator from the book
        response = self.client.post(f'/api/books/{self.book.id}/remove-collaborator/{self.user_collaborator.id}/')

        # Check if the collaborator was removed successfully
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the collaborator is no longer in the book's collaborators list
        self.book.refresh_from_db()
        self.assertTrue(self.user_collaborator not in self.book.collaborators.all())

    def test_add_collaborator_permission_denied(self):
        # Authenticate as the collaborator (not the author)
        self.client.force_authenticate(user=self.user_collaborator)

        # Try to add a collaborator (should be denied)
        response = self.client.post(f'/api/books/{self.book.id}/add-collaborator/{self.user_regular.id}/')

        # Check for a permission denied response
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_remove_collaborator_permission_denied(self):
        # Authenticate as the collaborator (not the author)
        self.client.force_authenticate(user=self.user_collaborator)

        # Try to remove a collaborator (should be denied)
        response = self.client.post(f'/api/books/{self.book.id}/remove-collaborator/{self.user_author.id}/')

        # Check for a permission denied response
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)