from rest_framework.routers import SimpleRouter

from .views import PostModelViewSet

router = SimpleRouter(trailing_slash=False)
router.register(prefix="posts", viewset=PostModelViewSet, basename="posts")
