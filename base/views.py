from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import View,TemplateView,FormView,DeleteView,CreateView
from django.urls import reverse_lazy
from api import models
from . import forms
from accounts.models import UserProfile
# Create your views here.

class IndexView(TemplateView):
    """Main index, shows journals and results of searches"""
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            context = super().get_context_data(**kwargs)
            context['user_journals'] = models.Journal.objects.filter(author=self.request.user)[:10]
            return context
    
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if self.request.method == 'POST':
            query = self.request.POST.get('search')
            journals = models.Journal.objects.filter(author=request.user)
            if query==None:
                results = models.Page.objects.filter(journal__in=journals)
            else:
                results = models.Page.objects.filter(journal__in=journals).filter(content__icontains=query)
            
            return render(request, "searched_pages.html", {'pages':results})
        else:
            return self.render_to_response(context)

class AboutView(TemplateView):
    """About template view"""
    template_name = 'about.html'

class DocumentationView(TemplateView):
    """Documentation template view"""
    template_name = 'how_to.html'

### JOURNALS ###

class JournalView(TemplateView):
    """Shows details of a specific journal"""
    template_name = 'journal.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['journal'] = get_object_or_404(models.Journal.objects.filter(author=self.request.user), 
        pk=self.kwargs['journal_id'])
        context['pages'] = models.Page.objects.filter(journal=self.kwargs['journal_id'])
        return context

class JournalCreateView(FormView):
    """Creates a journal using form"""
    template_name = 'model_create_form.html'
    form_class = forms.CreateJournalForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        title = form.cleaned_data['title']
        description = form.cleaned_data['description']
        author = self.request.user
        #check limit
        profile = get_object_or_404(UserProfile.objects.filter(user=author))
        if profile.count_journals < profile.journal_limit:
            journal = models.Journal(title=title,author=author,description=description)
            journal.save()
            #add journal
            profile.add_journal(1)
            return super().form_valid(form)
        else:
            return render(self.request,"limit_exceeded.html",{})

class JournalUpdateView(FormView):
    """Updates a journal using form"""
    template_name = 'edit_journal.html'
    form_class = forms.EditJournalForm
    success_url = ".."

    #old values inside new form
    def get_initial(self):
        initial = super(JournalUpdateView, self).get_initial()
        journal = get_object_or_404(models.Journal.objects.filter(author=self.request.user), 
        pk=self.kwargs['journal_id'])
        initial['title'] = journal.title
        initial['description'] = journal.description
        return initial

    def form_valid(self, form):
        journal = get_object_or_404(models.Journal.objects.filter(author=self.request.user), 
        pk=self.kwargs['journal_id'])
        journal.title = form.cleaned_data['title']
        journal.description = form.cleaned_data['description']
        journal.save()
        return super().form_valid(form)

class JournalDeleteView(DeleteView):
    """Deletes a journal, asks confirmation"""
    model = models.Journal
    template_name = "deletemodel.html"
    success_url = reverse_lazy('index')

    def form_valid(self,form):
        success_url = self.get_success_url()
        
        #subtract journal
        profile = get_object_or_404(UserProfile.objects.filter(user=self.request.user))
        profile.sub_journal(1)

        self.object.delete()
        return HttpResponseRedirect(success_url)
    
    def get_object(self):
        object = get_object_or_404(models.Journal.objects.filter(author=self.request.user), 
        pk=self.kwargs['journal_id'])

        return object

### PAGES ###

class PageView(TemplateView):
    """Shows details of a page"""
    template_name = 'page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = get_object_or_404(models.Page.objects.filter(pk=self.kwargs['page_id']))
        return context

class PageCreateView(FormView):
    """Creates a page using form with rich text formatting"""
    template_name = 'model_create_form.html'
    form_class = forms.CreatePageForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        content = form.cleaned_data['content']
        journal = get_object_or_404(models.Journal.objects.filter(author=self.request.user), 
        pk=self.kwargs['journal_id'])
        #check limit
        profile = get_object_or_404(UserProfile.objects.filter(user=self.request.user))
        if journal.count_pages < profile.pages_per_journal_limit:
            page = models.Page(journal=journal,content=content)
            page.save()
            journal.add_page(1)
            return super().form_valid(form)
        else:
            return render(self.request,"limit_exceeded.html",{})


class PageDeleteView(DeleteView):
    """Deletes a page"""
    model = models.Page
    template_name = "deletemodel.html"
    success_url = reverse_lazy('index')

    def form_valid(self,form):
        success_url = self.get_success_url()
        journal = get_object_or_404(models.Journal.objects.filter(pk=self.object.journal.pk))
        journal.sub_page(1)
        self.object.delete()
        return HttpResponseRedirect(success_url)

    def get_object(self):
        object = get_object_or_404(models.Page.objects.filter(pk=self.kwargs['page_id']))
        return object

class PageUpdateView(FormView):
    """Updates a page"""
    template_name = 'model_create_form.html'
    form_class = forms.CreatePageForm
    success_url = ".."

    def get_initial(self):
        initial = super(PageUpdateView, self).get_initial()
        page = get_object_or_404(models.Page.objects.filter(pk=self.kwargs['page_id']))
        initial['content'] = page.content
        return initial

    def form_valid(self, form):
        page = get_object_or_404(models.Page.objects.filter(pk=self.kwargs['page_id']))
        page.content = form.cleaned_data['content']
        page.save()
        return super().form_valid(form)
