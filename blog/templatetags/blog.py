from django.template import Library

register = Library()

@register.inclusion_tag('blog/post.html')
def blog_post(post):
    return {'post': post }