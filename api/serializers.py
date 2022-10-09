from rest_framework import serializers
from . import models

class JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Journal
        fields = [
            'pk',
            'title',
            'author',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['author','created_at','updated_at']

class PageSerializer(serializers.ModelSerializer):
    page_url = serializers.SerializerMethodField(read_only=True)#for renaming get_discount
    class Meta:
        model = models.Page
        fields = [
            'pk',
            'content',
            'journal',
            'page_url',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['journal','created_at','updated_at']
    
    def get_page_url(self, obj):
        """used to take absolute url of page"""
        return obj.get_absolute_url()