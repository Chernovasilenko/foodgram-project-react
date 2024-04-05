from rest_framework import mixins, response, viewsets


class PatchModelMixin:
    """Миксин для PATCH-запроса."""

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return response.Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class CreateListDestroyPatchMixin(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    PatchModelMixin,
    viewsets.GenericViewSet,
):
    """Миксин для GET, POST, DELETE и PATCH запросов."""
