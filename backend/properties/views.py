import re

from analytics.models import PropertyView, SearchHistory
from django.db.models import F
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from .filters import PropertyFilter
from .models import Property
from .search import build_property_queryset, parse_local_query
from .serializers import PropertySearchRequestSerializer, PropertySerializer


def normalize_query(value):
    normalized_query = re.sub(r"\s+", " ", value.strip().lower())
    return normalized_query


def get_client_ip(request):
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    return request.META.get("REMOTE_ADDR")


class IsLandlordOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user.is_authenticated
            and request.user.role == request.user.Roles.LANDLORD
        )


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class PropertyViewSet(viewsets.ModelViewSet):
    serializer_class = PropertySerializer
    permission_classes = [IsLandlordOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PropertyFilter
    search_fields = ["title", "description", "city", "district"]
    ordering_fields = ["price_per_night", "created_at", "views_count"]
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = Property.objects.select_related("owner").prefetch_related(
            "amenities"
        )

        if self.request.method in permissions.SAFE_METHODS:
            return queryset.filter(status=Property.Status.PUBLISHED)

        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        raw_query = request.query_params.get("search", "")
        normalized_query = normalize_query(raw_query)

        if normalized_query:
            try:
                SearchHistory.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    query=raw_query,
                    normalized_query=normalized_query,
                    city=request.query_params.get("city", ""),
                    property_type=request.query_params.get("property_type", ""),
                    price_min=request.query_params.get("price_min") or None,
                    price_max=request.query_params.get("price_max") or None,
                    rooms_min=request.query_params.get("rooms_min") or None,
                    rooms_max=request.query_params.get("rooms_max") or None,
                    results_count=response.data.get("count", 0),
                )
            except Exception:
                pass

        return response

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        rental_property = self.get_object()

        if (
            request.user.is_authenticated
            and rental_property.owner_id == request.user.id
        ):
            return response

        today = timezone.localdate()
        ip_address = get_client_ip(request)
        user_agent = request.META.get("HTTP_USER_AGENT", "")

        if request.user.is_authenticated:
            already_viewed = PropertyView.objects.filter(
                user=request.user,
                rental_property=rental_property,
                created_at__date=today,
            ).exists()
        else:
            already_viewed = PropertyView.objects.filter(
                user__isnull=True,
                rental_property=rental_property,
                ip_address=ip_address,
                created_at__date=today,
            ).exists()

        if not already_viewed:
            PropertyView.objects.create(
                user=request.user if request.user.is_authenticated else None,
                rental_property=rental_property,
                ip_address=ip_address,
                user_agent=user_agent,
            )

            Property.objects.filter(pk=rental_property.pk).update(
                views_count=F("views_count") + 1
            )

        return response

    @action(detail=False, methods=["get"], permission_classes=[permissions.AllowAny])
    def popular(self, request):
        queryset = self.get_queryset().order_by("-views_count")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["patch"], url_path="toggle-active")
    def toggle_active(self, request, pk=None):
        rental_property = self.get_object()

        if rental_property.status == Property.Status.PUBLISHED:
            rental_property.status = Property.Status.ARCHIVED
        else:
            rental_property.status = Property.Status.PUBLISHED

        rental_property.save(update_fields=["status", "updated_at"])

        serializer = self.get_serializer(rental_property)
        return Response(serializer.data)

    @extend_schema(
        request=PropertySearchRequestSerializer,
        responses=PropertySearchRequestSerializer,
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="search",
        permission_classes=[permissions.AllowAny],
    )
    def smart_search(self, request):
        request_serializer = PropertySearchRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        query = request_serializer.validated_data["query"]
        filters, confidence = parse_local_query(query)

        warnings = []
        if confidence == 0:
            return Response(
                {
                    "query": query,
                    "mode": "local",
                    "interpreted_filters": filters,
                    "results_count": 0,
                    "results": [],
                    "warnings": ["Could not confidently interpret the search query."],
                },
                status=status.HTTP_200_OK,
            )

        queryset = build_property_queryset(filters=filters)
        serializer = self.get_serializer(queryset, many=True)

        return Response(
            {
                "query": query,
                "mode": "local",
                "interpreted_filters": filters,
                "confidence": confidence,
                "results_count": queryset.count(),
                "results": serializer.data,
                "warnings": warnings,
            },
            status=status.HTTP_200_OK,
        )
