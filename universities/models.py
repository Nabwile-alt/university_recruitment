from django.db import models


class University(models.Model):
    name = models.CharField(max_length=200, unique=True)
    address = models.TextField()
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='university_logos/', null=True, blank=True)
    description = models.TextField(blank=True)
    founded_year = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Universities'
        ordering = ['name']

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=200)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='departments')
    description = models.TextField(blank=True)
    head = models.CharField(max_length=100, blank=True)

    class Meta:
        unique_together = ['name', 'university']
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.university.name}"
