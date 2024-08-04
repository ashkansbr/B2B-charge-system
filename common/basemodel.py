from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    id = models.UUIDField(_('id'), default=uuid.uuid4, primary_key=True, editable=False, db_index=True)
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated_at'), auto_now=True)

    class Meta:
        abstract = True
