from django.contrib import admin
from django.db import models
from .models import User, UserDetails
from django.contrib.gis.db import models
from mapwidgets.widgets import GooglePointFieldWidget


class PoiLocationInline(LeafletGeoAdminMixin, admin.StackedInline):
    model = UserDetails


class PointLocation(admin.ModelAdmin):
    formfield_overrides = {models.PointField: {"widget": GooglePointFieldWidget}}


admin.site.register(User)
admin.site.register(UserDetails, PoiLocationInline)
