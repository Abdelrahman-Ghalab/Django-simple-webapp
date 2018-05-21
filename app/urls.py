import views

from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
    url(r'^register/', views.register),
    url(r'^logout/$', views.loggingout),
    url(r'^login/$', views.loginngin),
    url(r'^add_vacation/$', views.add_vacation),
    url(r'^edit_vacation/$', views.updateVacation),


]
#(?P<string>[\w\-]+)/
