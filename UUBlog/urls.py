from django.contrib import admin
from django.urls import path,re_path

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from  blog.views import view
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^index/', view.index),
    re_path(r'^login/', view.login),
    re_path(r'^upload/', view.uploadImg),
    re_path(r'^show/', view.showImg),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  这句话是用来指定和映射静态文件的路径

urlpatterns += staticfiles_urlpatterns()
