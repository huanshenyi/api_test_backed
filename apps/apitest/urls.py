__author__ = "ハリネズミ"
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter(trailing_slash=False)
router.register("project", views.ProjectViewSets, basename="project")
router.register("host", views.HostViewSets, basename="host")

app_name = "apitest"
urlpatterns = [

] + router.urls
