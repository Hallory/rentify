from django.db import models


class Favorite(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="favorites")
    rental_property = models.ForeignKey("properties.Property", on_delete=models.CASCADE, related_name="favorites")
    created_at = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        unique_together = ("user", "rental_property")
        ordering = ["-created_at"]
        verbose_name = "Favorite"
        verbose_name_plural = "Favorites"

    def __str__(self):
        return f"{self.user} - {self.rental_property}"
    