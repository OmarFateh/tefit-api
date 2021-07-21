from rest_framework import serializers

from .utils import datetime_to_string, rounded_timesince


class PostReadTimeViewCountMixinSerializer(serializers.Serializer):
    """
    Post read time and views count mixin serializer.
    """
    views_count = serializers.SerializerMethodField()
    read_time = serializers.SerializerMethodField()

    def get_views_count(self, obj):
        return obj.views_count

    def get_read_time(self, obj):
        return obj.read_time


class TimestampMixinSerializer(serializers.Serializer):
    """
    Timestamp mixin serializer.
    """
    updated_at = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    timesince = serializers.SerializerMethodField()

    def get_updated_at(self, obj):
        return datetime_to_string(obj.updated_at)

    def get_created_at(self, obj):
        return datetime_to_string(obj.created_at)

    def get_timesince(self, obj):
        return f"{rounded_timesince(obj.created_at)} ago"
