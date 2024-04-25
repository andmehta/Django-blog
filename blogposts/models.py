from django.db import models
from django.contrib.auth import get_user_model


class BlogPost(models.Model):
    """Basic model for a Blog Post"""

    title = models.CharField(null=True, max_length=50)
    content = models.CharField()
    # Since it's against best practices to delete users (should always deactivate) The decision on what to do on_delete
    #  Doesn't REALLY matter. But I think just having an author-less blogpost makes the most sense
    author = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL)
