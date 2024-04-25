from rest_framework.viewsets import ModelViewSet
from blogposts.serializers import BlogPostSerializer
from blogposts.models import BlogPost


class BlogPostViewSet(ModelViewSet):
    serializer_class = BlogPostSerializer
    queryset = BlogPost.objects.all()
