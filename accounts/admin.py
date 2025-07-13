from django.contrib import admin
from .models import Profile,Review
from .models import TrainerRequest,Appointments,Workouts,DailyEntry
from django.contrib.auth.models import Group
from .admin_site import custom_admin_site
# Register your models here.
admin.site.register(Profile)
admin.site.register(Review)
admin.site.register(Appointments)
admin.site.register(Workouts)
admin.site.register(DailyEntry)
class TrainerRequestAdmin(admin.ModelAdmin):
    list_display=['user','message','status','created_at']
    list_filter=['status']
    actions = ['approve_requests','reject_requests']

    def approve_requests(self, request, queryset):
        trainer_group = Group.objects.get(name='trainer')
        for obj in queryset:
            if obj.status!= 'approved':
                obj.status = 'approved'
                obj.save()
                obj.user.groups.clear()
                obj.user.groups.add(trainer_group)
                obj.user.profile.role = 'trainer'
        self.message_user(request,'Selected requests have been approved')

    def reject_requests(self,request,queryset):
        for obj in queryset:
            if obj.status!='rejected':
                obj.status = 'rejected'
                obj.save()
        self.message_user(request,'Selected request have been rejected')

    approve_requests.short_description = 'Approve selected trainer requests'
    reject_requests.short_description = 'Reject selected trainer requests'

custom_admin_site.register(TrainerRequest,TrainerRequestAdmin)
custom_admin_site.register(Profile)
admin.site.register(TrainerRequest,TrainerRequestAdmin)