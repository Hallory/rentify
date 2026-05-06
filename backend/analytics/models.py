from django.db import models


class SearchHistory(models.Model):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="search_history",
    )
    query = models.CharField(max_length=255)
    normalized_query = models.CharField(max_length=255)
    city = models.CharField(max_length=100, blank=True)
    property_type = models.CharField(max_length=50, blank=True)
    price_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    price_max = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    rooms_min = models.PositiveIntegerField(blank=True, null=True)
    rooms_max = models.PositiveIntegerField(blank=True, null=True)
    results_count = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Search History"
        verbose_name_plural = "Search Histories"
        ordering = ["-created_at"]