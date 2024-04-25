from django.urls import path

from blogposts.views import BlogPostViewSet

urlpatterns = [
    path("", BlogPostViewSet.as_view({"get": "list"})),
]