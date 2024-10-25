from django.contrib import admin
from .models import Profile, Skill, SkillTrade, Rating, SkillRequest, Notification

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'skills', 'experience', 'rating')  # Customize the fields to display
    search_fields = ('user__username',)  # Allow searching by username

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('skill_name', 'user', 'rating')  # Fields to display in the admin list view
    search_fields = ('skill_name', 'user__username')  # Add search functionality based on skill name

@admin.register(SkillTrade)
class SkillTradeAdmin(admin.ModelAdmin):
    list_display = ('offered_by', 'offered_skill', 'requested_by', 'requested_skill', 'status')
    list_filter = ('status',)  # Add filter based on status ('pending', 'accepted', etc.)
    search_fields = ('offered_skill__skill_name', 'requested_skill__skill_name')

@admin.register(SkillRequest)
class SkillRequestAdmin(admin.ModelAdmin):
    list_display = ('requester', 'skill', 'created_at')
    search_fields = ('requester__username', 'skill__skill_name')

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'skill', 'score')
    search_fields = ('user__username', 'skill__skill_name')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_viewed', 'created_at')
    list_filter = ('is_viewed',)  # Add a filter for viewed/unviewed notifications
    search_fields = ('message',)
