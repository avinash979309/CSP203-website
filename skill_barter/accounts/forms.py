from allauth.account.forms import SignupForm
from django import forms
from .models import Profile
from .models import Skill
from .models import Message


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user
    

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['skills', 'experience', 'rating','profile_picture']






class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['skill_name', 'description', 'rating']  # Fields for the skill form





class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Type your message here...'}),
        }
