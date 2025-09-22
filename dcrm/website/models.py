from django.db import models
from django.conf import settings


class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=20)

    def __str__(self):
        return (f"{self.first_name} {self.last_name}")


class Exercise(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    exercise_name = models.CharField(max_length=50)
    exercise_description = models.TextField()
    exercise_sets = models.PositiveIntegerField(default=3)
    exercise_reps = models.PositiveIntegerField(default=8)
    exercise_weight = models.FloatField(null=True, blank=True)
    exercise_rest = models.PositiveIntegerField(default=60)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="exercises"
    )

    def __str__(self):
        return (f"{self.exercise_name}")


class Plan(models.Model):
    plan_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="plans"
    )
    exercises = models.ManyToManyField("Exercise", related_name="plans", blank=True)
    last_executed = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.plan_name
