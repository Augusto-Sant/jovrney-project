from django.shortcuts import render,get_object_or_404
from django.views.generic import View,TemplateView
from rest_framework import generics,response
from . import models
from . import serializers
from accounts.models import UserProfile
# Create your views here.

### REST API --

##Journals
class JournalListCreateAPIView(generics.ListCreateAPIView):
    """List all journals or create new journal for current user | API VIEW"""
    serializer_class = serializers.JournalSerializer

    def perform_create(self, serializer):
        #check limit
        profile = get_object_or_404(UserProfile.objects.filter(user=self.request.user))
        if profile.count_journals < profile.journal_limit:
            #add journal
            profile.add_journal(1)
            serializer.save(author=self.request.user)
    
    def get_queryset(self):
        #this limits the view only for current user
        return models.Journal.objects.filter(author=self.request.user)

class JournalDetailAPIView(generics.RetrieveAPIView):
    """Detail of a Specific Journal of current user based on its pk | API VIEW"""
    serializer_class = serializers.JournalSerializer
    lookup_url_kwarg = 'journal_id' #change url argument from pk to journal_id
    #i need to make router for retrieve api to work
    def get_queryset(self):
        return models.Journal.objects.filter(author=self.request.user)

class JournalUpdateAPIView(generics.UpdateAPIView):
    """Updates a journal using PUT Request on API"""
    serializer_class = serializers.JournalSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'journal_id'

    def get_queryset(self):
        return models.Journal.objects.filter(author=self.request.user)
    
    def perform_update(self, serializer):
        instance = serializer.save()

class JournalDestroyView(generics.DestroyAPIView):
    """Class that deletes a Journal | depends on DELETE"""
    serializer_class = serializers.JournalSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'journal_id'

    def get_queryset(self):
        return models.Journal.objects.filter(author=self.request.user)

    def perform_destroy(self, instance):
        profile = get_object_or_404(UserProfile.objects.filter(user=self.request.user))
        profile.sub_journal(1)
        super().perform_destroy(instance)

##Pages
class PageListCreateAPIView(generics.ListCreateAPIView):
    """Class takes all pages from a specific author of a journal in url| GET to take list of pages"""
    serializer_class = serializers.PageSerializer

    def perform_create(self, serializer):
        self.journal = get_object_or_404(models.Journal.objects.filter(author=self.request.user), pk=self.kwargs['journal_id'])
        profile = get_object_or_404(UserProfile.objects.filter(user=self.request.user))
        if self.journal.count_pages < profile.pages_per_journal_limit:
            self.journal.add_page(1)
            serializer.save(journal=self.journal)

    def get_queryset(self):
        self.journal = get_object_or_404(models.Journal.objects.filter(author=self.request.user), pk=self.kwargs['journal_id'])
        return models.Page.objects.filter(journal=self.journal.pk)

class PageDetailAPIView(generics.RetrieveAPIView):
    """Detail of a Specific page of current user based on its pk"""
    serializer_class = serializers.PageSerializer
    lookup_url_kwarg = 'page_id'
    def get_queryset(self):
        self.journal = get_object_or_404(models.Journal.objects.filter(author=self.request.user), pk=self.kwargs['journal_id'])
        return models.Page.objects.filter(journal=self.journal.pk)

class PageUpdateAPIView(generics.UpdateAPIView):
    """Updates a page using PUT request in API"""
    serializer_class = serializers.PageSerializer
    lookup_field = 'pk' #field to find
    lookup_url_kwarg = 'page_id'
    def get_queryset(self):
        self.journal = get_object_or_404(models.Journal.objects.filter(author=self.request.user), pk=self.kwargs['journal_id'])
        return models.Page.objects.filter(journal=self.journal.pk)
    
    def perform_update(self, serializer):
        instance = serializer.save()

class PageDestroyAPIView(generics.DestroyAPIView):
    """Class that deletes a product | depends on DELETE"""
    serializer_class = serializers.PageSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'page_id'
    
    def get_queryset(self):
        self.journal = get_object_or_404(models.Journal.objects.filter(author=self.request.user), pk=self.kwargs['journal_id'])
        self.journal.sub_page(1)
        return models.Page.objects.filter(journal=self.journal.pk)

    def perform_destroy(self, instance):
        super().perform_destroy(instance)


##Search

class PageSearchAPIView(generics.ListAPIView):
    """Search like /api/journals/{journal_id}/pages/search?q={query} on API"""
    serializer_class = serializers.PageSerializer

    def get_queryset(self,*args,**kwargs):
        self.journal = get_object_or_404(models.Journal.objects.filter(author=self.request.user), pk=self.kwargs['journal_id'])
        query = self.request.GET.get('q')
        if query==None:
            return models.Page.objects.filter(journal=self.journal.pk)
        results = models.Page.objects.filter(journal=self.journal.pk).filter(content__icontains=query)
        return results