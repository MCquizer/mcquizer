
from django.conf.urls import include, url
from django.contrib import admin
from quizer import views

urlpatterns = [
	url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.main_page, name='quizer.views.index'),
	url(r'^main_page.html$', views.main_page, name='main_page'),
    url(r'^user/$', views.user_page, name='user_page'),
    
    url(r'^login/$','django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^logout/$', views.logout_page, name='logout_page'),
    url(r'^register/$', views.register_page, name='register_page'),
    url(r'^registration/register_success.html', views.register_success_page, name='register_success_page'),
    url(r'^save/$', views.question_save_page, name='question_save_page'),
    url(r'^quiz/(?P<quiz_id>.+?)/$', views.quiz, name='quiz'),
    url(r'^result/score/(?P<quiz_id>.+?)/$', views.get_score, name='get_score'),
    url(r'^score/(?P<quiz_id>.+?)/$', views.score, name='score'),
    url(r'^set_date/(?P<quiz_id>.+?)/$', views.set_date, name='set_date'),
]
