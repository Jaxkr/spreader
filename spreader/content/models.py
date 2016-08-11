from django.db import models
import random
import datetime
import hashlib
import time
from django.utils import timezone

# Create your models here.

class PoolEntry(models.Model):
    post = models.ForeignKey('ImagePost')
    time_added = models.DateTimeField(default=timezone.now)
    unique_id = models.CharField(max_length=64, blank=True, unique=True)

    def save(self, *args, **kwargs):
        h = hashlib.new('sha256')
        to_hash = str(random.random()) + str(time.time())
        h.update(to_hash.encode('utf-8'))
        hashed = h.hexdigest()
        self.unique_id = hashed
        super(PoolEntry, self).save(*args, **kwargs)


class ImagePost(models.Model):
    url = models.CharField(max_length=2000)
    caption = models.CharField(max_length=1000)
    views = models.IntegerField(default=0)
    spread = models.IntegerField(default=0)
    time_added = models.DateTimeField(default=timezone.now)

class Comment(models.Model):
    comment_text = models.CharField(max_length=300)
    time_added = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey('ImagePost')
