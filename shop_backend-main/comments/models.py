from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

User: models.Model = get_user_model()

# Create your models here.
class Comment(models.Model):
    object_id = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    contenttype = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey("contenttype", "object_id")
    content = models.TextField()
    is_approved = models.BooleanField(default=False)
    parent = models.ForeignKey("self", null=True, blank=True,
                               on_delete=models.CASCADE, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes =

    @property
    def is_reply(self):
        return self.parent is not None
