from django.urls import path
from . import views

app_name = 'base'

urlpatterns = [
    ##search
    path("search",views.SearchView.as_view()),
    ##journals
    path("journals/<int:journal_id>/",views.JournalView.as_view()),
    path("journals/create/",views.JournalCreateView.as_view(),name="create_journal"),
    path("journals/<int:journal_id>/delete/",views.JournalDeleteView.as_view()),
    path("journals/<int:journal_id>/update/",views.JournalUpdateView.as_view()),
    ##pages
    path("journals/<int:journal_id>/pages/<int:page_id>/",views.PageView.as_view()),
    path("journals/<int:journal_id>/create/",views.PageCreateView.as_view()),
    path("journals/<int:journal_id>/pages/<int:page_id>/delete/",views.PageDeleteView.as_view()),
    path("journals/<int:journal_id>/pages/<int:page_id>/update/",views.PageUpdateView.as_view()),
]