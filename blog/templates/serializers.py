from rest_framework.serializers import ModelSerializer
from blog.models import Post


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title','text','created_date','published_date')
        read_only_fields = ['id','created_date','published_date']
