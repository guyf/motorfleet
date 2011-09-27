from django.contrib import admin
from motorfleet.models import *

admin.site.register(Fleet)
admin.site.register(MotorfleetProfile)
admin.site.register(Policy)
admin.site.register(Claim)
admin.site.register(Conviction)
admin.site.register(Vehicle)

