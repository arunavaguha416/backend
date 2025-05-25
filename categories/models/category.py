from django.db import models
from authentication.models import User
from budget_tracker.softDeleteModel import SoftDeletionModel
import uuid
from django.utils.translation import gettext_lazy as _


class Category(SoftDeletionModel):
    id = models.UUIDField(primary_key=True, 
                        default=uuid.uuid4, 
                        editable=False, 
                        unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')