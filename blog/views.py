from django import views
from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from rest_framework import viewsets
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from blog.templates.serializers import PostSerializer
from .models import Post
from .forms import PostForm


class PostViewSet(viewsets.ViewSet):
    renderer_classes = [TemplateHTMLRenderer]

    def create(self,request):
        data = request.data
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            post = serializer.save(
                author = request.user,
                published_date=timezone.now()
            )
            return self.retrieve(request, post.id)
        else:
            return Response({'form':serializer}, template_name='blog/post_edit.html')




    def retrieve(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post)
        return Response({'post': serializer.data}, template_name='blog/post_detail.html')

    def list(self, request):
        edit = request.query_params.get('edit', False)
        if edit:
            serializer=PostSerializer()
            return Response({'form': serializer}, template_name='blog/post_edit.html')
        else:
            posts = Post.objects.all()
            serializer = PostSerializer(posts, many=True)
            return Response({'posts': serializer.data}, template_name='blog/post_list.html')



class PostListView(TemplateView):
    template_name = 'blog/post_list.html'
    def get_context_data(self):
        return {'posts': Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')}


class PostDetailsView(views.View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        return render(request, 'blog/post_detail.html', {'post': post})


class PostNewView(views.View):
    template_name = 'blog/post_edit.html'

    def post(self, request):
       form = PostForm(request.POST)
       if form.is_valid():
           post = form.save(commit=False)
           post.author = request.user
           post.published_date = timezone.now()
           post.save()
           return redirect('post_detail', pk=post.pk)
       else:
           return render(request, self.template_name, {'form': form})

    def get(self, request):
        return render(request, self.template_name, {'form': PostForm()})


class PostEditView(views.View):
    template_name = 'blog/post_edit.html'

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
        else:
            return render(request, self.template_name, {'form': form})

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = PostForm(instance=post)
        return render(request, self.template_name, {'form': form})

