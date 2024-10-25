from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    skills = models.TextField(blank=True)  # Comma-separated skills
    experience = models.PositiveIntegerField(default=0)  # Years of experience
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)  # User rating (0-5)

    def __str__(self):
        return f'{self.user.username} Profile'


class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='skills')  # Link skill to a user
    skill_name = models.CharField(max_length=100)  # Name of the skill
    description = models.TextField(blank=True, null=True)  # Optional description of the skill
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)  # Optional rating for the skill
    rating_count = models.IntegerField(default=0)  # To track how many ratings a skill has

    def __str__(self):
        return self.skill_name


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE,related_name='ratings')
    score = models.PositiveIntegerField()  # Rating score (1 to 5)

    class Meta:
        unique_together = ('user', 'skill')  # Ensure a user can only rate a skill once

    def __str__(self):
        return f"{self.user.username} rated {self.skill.skill_name} - {self.score}"


class SkillRequest(models.Model):
    requester = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request by {self.requester.username} for {self.skill.skill_name}"


class SkillTrade(models.Model):
    offered_by = models.ForeignKey(User, related_name='offered_by', on_delete=models.CASCADE)
    offered_skill = models.ForeignKey(Skill, related_name='offered_skill', on_delete=models.CASCADE)
    requested_skill = models.ForeignKey(Skill, related_name='requested_skill', on_delete=models.CASCADE)
    requested_by = models.ForeignKey(User, related_name='requested_by', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')], default='pending')
    prerequisites = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.offered_by} offers {self.offered_skill} for {self.requested_by}'s {self.requested_skill}"
    

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_viewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification for {self.user.username}: {self.message}'




class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username} to {self.receiver.username}: {self.content}'

