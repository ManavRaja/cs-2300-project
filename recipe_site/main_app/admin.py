from django.contrib import admin

from .models import *

# Register your models here.
# 
# apparently Recipe model cannot be registered with admin b/c 
# it is an abstract model
# admin.site.register(Recipe)
admin.site.register(PremadeRecipe)
admin.site.register(CustomRecipe)
admin.site.register(WeeklyMealPlan)