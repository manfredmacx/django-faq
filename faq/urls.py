from django.conf.urls.defaults import patterns, url

import views

urlpatterns = patterns('',
    url(r'^$', views.faq_list_by_group, name='faq'),
    url(r'^question/(?P<question_slug>[-\w]+)$', views.question_detail, name='question-detail'),
    url(r'^submit$', views.submit_faq, name='submit'),
)
