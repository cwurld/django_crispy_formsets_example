from django.conf.urls import patterns, url, include
from django.conf.urls.static import static
from django.conf import settings

import views

urlpatterns = patterns(
    '',
    url(r'^create/$', views.ParentCreate.as_view(), name='create_parent'),
    url(r'^update/(?P<pk>\d+)/$', views.ParentUpdate.as_view(), name='update_parent'),
    url(r'^$', views.ParentList.as_view(), name='list_parents'),
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)