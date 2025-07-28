from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()

class MessagingTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass1234')
        self.user2 = User.objects.create_user(username='user2', password='pass1234')
        self.token = RefreshToken.for_user(self.user1).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_create_conversation_and_send_message(self):
        # Create conversation
        response = self.client.post('/api/conversations/', {
            'participants': [self.user2.id]
        })
        self.assertEqual(response.status_code, 201)
        conv_id = response.data['conversation_id']

        # Send message
        response = self.client.post(f'/api/conversations/{conv_id}/send_message/', {
            'message_body': 'Test message'
        })
        self.assertEqual(response.status_code, 201)

    def test_unauthenticated_access(self):
        self.client.credentials()  # Remove auth
        response = self.client.get('/api/conversations/')
        self.assertEqual(response.status_code, 401)
