__author__ = "ハリネズミ"
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("project", views.ProjectSerializer, basename="project")

app_name = "apitest"
urlpatterns = [

] + router.urls
