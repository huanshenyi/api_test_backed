__author__ = "ハリネズミ"
from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path

router = DefaultRouter(trailing_slash=False)
router.register("project", views.ProjectViewSets, basename="project")
router.register("host", views.HostViewSets, basename="host")
router.register("api", views.ApiViewSets, basename="api")

app_name = "apitest"
urlpatterns = [
   path('run/api/<int:api_id>', views.RunApiView.as_view(), name="run_api")
] + router.urls
