from rest_framework import viewsets, status
from rest_framework.views import Response
from rest_framework import permissions
from .serializers import EnterprisePlanListSerializer, BasicPlanListSerializer, PremiumPlanListSerializer
from .models import UserImages
from datetime import timedelta
from django.utils import timezone

class UserImagesViewSet(viewsets.ModelViewSet):
    """
    Viewset responsible for filtering and showing images using
    serializers depending on user's plan, and supporting post new image
    """
    queryset = UserImages.objects.all()
    serializer_class = BasicPlanListSerializer
    permission_classes = [permissions.IsAuthenticated]
    premium_serializer_class = PremiumPlanListSerializer
    enterprise_serializer_class = EnterprisePlanListSerializer

    def get_serializer_class(self):
        """
        Simple filtering with serializers depending
        on the user's set plan in the Profile model
        """
        if self.action == 'list' or 'post':
            try:
                user_tier = self.request.user.user_profile.user_tier.name
                if user_tier == 'Basic':
                    return self.serializer_class
                elif user_tier == 'Premium':
                    return self.premium_serializer_class
                elif user_tier == 'Enterprise':
                    return self.enterprise_serializer_class
                else:
                    return self.serializer_class
            except AttributeError:
                return self.serializer_class
        return super(UserImagesViewSet, self).get_serializer_class()

    def get_queryset(self):
        """
        Shows queryset and link removal support for
        Enterprise plan when expire_time field is specified
        """
        user = self.request.user
        qs = UserImages.objects.filter(user=user)
        for image in qs:
            if image.expire_time != 0:
                time = image.published_date + timedelta(seconds=image.expire_time)
                if time < timezone.now():
                    image.delete()
                    return qs
        return qs

    def post(self, request, format=None):
        user = self.get_object()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)