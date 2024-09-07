from rest_framework.routers import SimpleRouter

from .views import UserModelViewSet

router = SimpleRouter(trailing_slash=False)
router.register(prefix="users", viewset=UserModelViewSet, basename="users")
