from rest_framework import serializers
from .models import Tag, Entry
from django.contrib.auth import get_user_model

User = get_user_model()

class TagSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tag
        field = ["id", "name"]

class EntrySerializers(serializers.ModelSerializer):
    tags = TagSerializers(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,  
        write_only=True,
        source="tags"
    )
    author_username = serializers.CharField(
        source="author.username",
        read_only=True
        )

    class Meta:
        model = Entry
        field = [
            "id",
            "title",
            "tags",
            "tag_id",
            "context",
            "create",
            "update",
            "author_username",
            ]
        read_only_field = [
            "id",
            "created",
            "update",
            "author_username"
        ]

    def create(self, validate_data):
        tags = validate_data.pop("tags", [])
        entry = Entry.objects.create(**validate_data)
        entry.tags.set(tags)
        return entry
    