from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'api'

urlpatterns = [
    path('auth/', obtain_auth_token), #token for rest api requests
    #journals
    path("journals/",views.JournalListCreateAPIView.as_view()),
    path("journals/<int:journal_id>/",views.JournalDetailAPIView.as_view()),
    path("journals/<int:journal_id>/update/",views.JournalUpdateAPIView.as_view()),
    path("journals/<int:journal_id>/delete/",views.JournalDestroyView.as_view()),
    #pages
    path("journals/<int:journal_id>/pages/",views.PageListCreateAPIView.as_view()),
    path("journals/<int:journal_id>/pages/<int:page_id>/",views.PageDetailAPIView.as_view()),
    path("journals/<int:journal_id>/pages/<int:page_id>/update/",views.PageUpdateAPIView.as_view()),
    path("journals/<int:journal_id>/pages/<int:page_id>/delete/",views.PageDestroyAPIView.as_view()),
    #Search
    path("journals/<int:journal_id>/pages/search",views.PageSearchAPIView.as_view()),
]