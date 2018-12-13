from django.shortcuts import render, redirect

# Create your views here.
from rest_framework import request
from comments.forms import CommentForm


class CommentView(views.View):
    def post(self):
        redirect_url =request.get('redirect_url')
        form = CommentForm(request.POST)
        if form.is_valid():
            form.seve()
        else:

            pass
            # TODO ahow errors to user
        return redirect(redirect_url)
