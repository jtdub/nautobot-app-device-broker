"""Django urlpatterns declaration for device_broker app."""

from django.templatetags.static import static
from django.urls import path
from django.views.generic import RedirectView
from nautobot.apps.urls import NautobotUIViewSetRouter

# Uncomment the following line if you have views to import
# from device_broker import views


app_name = "device_broker"
router = NautobotUIViewSetRouter()

# Here is an example of how to register a viewset, you will want to replace views.DeviceBrokerUIViewSet with your viewset
# router.register("device_broker", views.DeviceBrokerUIViewSet)


urlpatterns = [
    path("docs/", RedirectView.as_view(url=static("device_broker/docs/index.html")), name="docs"),
]

urlpatterns += router.urls
