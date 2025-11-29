from comments.models import Comment

from rest_framework import serializers


class Commentserializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
