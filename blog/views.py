from datetime import timedelta
from django import views
from django.core.checks import messages
from django.core.mail import send_mail
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
        print('---------------', request)
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

    def update(self, request,pk):
        pass



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

class RestorePasswordView(views.View):
    templete_name ='password/restor_password.html'

    def get(self, request):
        form = RestorePasswordForm()
        return render(request, self.templete_name, {'form':form})

    def post(self, request):
        form = RestorePasswordForm(request.POST)
        if form.is_valid():
            email = form.clesn_date['email']
            user = get_object_or_404(User, email=email)
            token = self.generate_token()
            resore_token = RestorePasswordToken(
                token = token,
                expire_date = timezone.now()+timedelta(day=3),
                user = user
            )
            resore_token.seve()

            send_mail(
                subject='Ссылка на восстанолвление пароля',
                message=self.create_restore_email_message(resore_token),
                from_email='blog@mail.com',
                recipient_list=[email]
            )
            messages.success(request,'Вам отправленна ссылка на изменение пароля на почту.')

class ResetPasswordView(views.View):
    temolete_name ='password/reset_password.html'

    def get_context_date(self):
        return {'form': ResetPasswordForm()}

    def get(self, request):
        self.get_valid_token(request)
        super().get(request)

    def post(self,request):
        token = rquest.GET['token']
        restore_token = get_object_or_404(RestorePasswordToken)
        if not restore_token.is_valid:
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                user = restore_token.user
                user.set_password(form.cleaned_data['password'])
                return redirect(request, 'admin/')
        else:
            messages.error('Срока ссылки истек')

    def get_valid_token(self,request):
        token = rquest.GET['token']
        restore_token = get_object_or_404(RestorePasswordToken)
        if restore_token.is_expired:
            raise Http404('Токен')
        return restore_token


        return render(request, self.temolete_name, {'form': ResetPasswordForm})