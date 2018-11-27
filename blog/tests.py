from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from blog.models import Post

# Create your tests here.
from blog.templates.serializers import PostSerializer


class BlogAPITestCase(TestCase):



    def setUp(self):
        super().setUp()

        self.user = User.objects.create()

        self.posts = [
            Post.objects.create(title='Title1',
                                text='Text test123',
                                author=self.user),
            Post.objects.create(title='Title2',
                                text='Text test12322222',
                                author=self.user),
        ]
        self.client=APIClient()

    def test_post_list(self):
        expected ={
            'posts':[
                PostSerializer(p).data for p in self.posts

            ]
        }
        response = self.client.get('/posts/')
        self.assertEqual(response.data, expected)

    def test_posts_retriever(self):

        response = self.client.get('/posts/{}/'.format(self.posts[0].id))

        data = response.data
        self.assertIn('post',data)
        post = data['post']

        epost = self.posts[0]
        self.assertEqual(post.get('id',None), epost.id)
        self.assertEqual(post.get('title',None), epost.title)

    def test_posts_create(self):
        data = {
           'title':'',
            'text': 'T2323itle1'
        }

        self.client.force_authenticate(self.user)

        response = self.client.post('/posts/', data=data)