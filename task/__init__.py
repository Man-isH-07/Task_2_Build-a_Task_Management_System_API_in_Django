from __future__ import absolute_import, unicode_literals
# Ensuring that Celery is loaded when Django starts
from core.celery import app as celery_app

__all__ = ('celery_app',)
