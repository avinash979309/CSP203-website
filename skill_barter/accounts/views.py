# accounts/views.py

from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from .models import Profile
from .forms import ProfileForm,SkillForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Skill,SkillTrade,Notification
from django.contrib.auth.models import User
from django.core.paginator import Paginator  # Import Paginator
from django.views.generic import View

#this is custom login view
class CustomLoginView(LoginView):
    template_name = 'login.html'

    # Override form_valid to redirect to the home page after successful login
    def form_valid(self, form):
        login(self.request, form.get_user())
        return redirect('home')
    



class LogoutView(View):

    def get(self, request):
        return redirect('login')



# Custom Registration View
def RegisterView(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            # Authenticate the newly created user and log them in
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home page after successful registration
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


@login_required
def view_profile(request, user_id=None):
    # Display the logged-in user's profile, ignore passed user_id
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'accounts/profile.html', {'profile': profile})


@login_required
def edit_profile(request, user_id):
    profile = get_object_or_404(Profile, id=user_id)  # Get the profile
    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES, instance=profile)  # Bind the profile instance to the form
        if form.is_valid():
            form.save()
            skill_name=form.cleaned_data['skills']
            save_skill=Skill(skill_name=skill_name)
            save_skill.user = request.user
            save_skill.save()
              # Save the updated profile
            return redirect('profile',user_id=user_id)  # Redirect to the profile page after saving
    else:
        form = ProfileForm(instance=profile)  # Create a form instance with the current profile data
    return render(request, 'accounts/edit_profile.html', {'form': form, 'profile': profile})  # Render the edit profile page



@login_required
def search_profiles(request):
    query = request.GET.get('q')
    
    # Get the current user's skills
    current_user_skills = Skill.objects.filter(user=request.user).values_list('skill_name', flat=True)
    
    if query:
        # Filter profiles based on the query, but exclude users who only have skills the current user already has
        profiles = Profile.objects.filter(
            (Q(skills__icontains=query) | Q(user__username__icontains=query)) &
            ~Q(skills__in=current_user_skills)
        )
    else:
        # Filter profiles that don't contain the current user's skills
        profiles = Profile.objects.exclude(skills__in=current_user_skills)
    
    return render(request, 'accounts/search.html', {'profiles': profiles})




# accounts/views.py

@login_required
def add_skill(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = request.user
            skill.save()

            # Create a notification for the user
            Notification.objects.create(
                user=request.user,
                message=f"You have added a new skill: {skill.skill_name}."
            )

            return redirect('skill_list')
    else:
        form = SkillForm()

    return render(request, 'add_skill.html', {'form': form})


@login_required
def skill_list(request):
    query = request.GET.get('q', '')

    # Get the current user's skills
    current_user_skills = Skill.objects.filter(user=request.user).values_list('skill_name', flat=True)

    # Filter skills based on query, excluding the current user's skills
    if query:
        skills = Skill.objects.filter(
            Q(skill_name__icontains=query) | Q(description__icontains=query)  # noqa: E0602
        ).exclude(skill_name__in=current_user_skills)
    else:                                                                           
        # If no query, exclude skills the current user already possesses
        skills = Skill.objects.exclude(skill_name__in=current_user_skills)

    paginator = Paginator(skills, 5)  # Show 5 skills per page
    page_number = request.GET.get('page')  # Get the current page number
    skills_page = paginator.get_page(page_number)  # Get skills for that page

    return render(request, 'skill_list.html', {'skills': skills_page, 'query': query})  # Pass paginated skills to template



@login_required
def initiate_trade(request):
    # Get the user's own skills
    user_skills = Skill.objects.filter(user=request.user)

    # Get skills available for trade by excluding the user's skills
    available_skills_to_trade = Skill.objects.exclude(user=request.user)

        # Get the preselected skill ID from the query parameters
    preselected_skill_id = request.GET.get('skill_id')
    preselected_skill = None
    if preselected_skill_id:
        preselected_skill = get_object_or_404(Skill, id=preselected_skill_id)

    if request.method == 'POST':
        skill_id = request.POST.get('skill_id')  # Skill the user wants to trade for
        offered_skill_id = request.POST.get('offered_skill')  # Skill the user offers in return
        prerequisites = request.POST.get('prerequisites', '')  # Any prerequisites (optional)

        if not skill_id or not offered_skill_id:
            return render(request, 'initiate_trade.html', {
                'user_skills': user_skills,
                'available_skills': available_skills_to_trade,
                'preselected_skill': preselected_skill,
                'error': 'Please select both a skill to trade for and a skill to offer.'
            })

        # Get the requested skill and offered skill based on their IDs
        skill = get_object_or_404(Skill, id=skill_id)  # Requested skill by another user
        offered_skill = get_object_or_404(Skill, id=offered_skill_id)  # Skill offered by the current user

        # Validate that the offered skill belongs to the current user
        if offered_skill.user != request.user:
            return render(request, 'initiate_trade.html', {
                'user_skills': user_skills,
                'available_skills': available_skills_to_trade,
                'preselected_skill': preselected_skill,
                'error': 'You do not own this skill. Please select one of your own skills to offer.'
            })

        # Ensure that the user is not trading the same skill for itself
        if offered_skill == skill:
            return render(request, 'initiate_trade.html', {
                'user_skills': user_skills,
                'available_skills': available_skills_to_trade,
                'preselected_skill': preselected_skill,
                'error': 'You cannot trade a skill for itself.'
            })

        # Create the trade request for the user
        trade = SkillTrade.objects.create(
            offered_by=request.user,
            offered_skill=offered_skill,
            requested_skill=skill,
            requested_by=skill.user,  # Owner of the requested skill
            prerequisites=prerequisites
        )

        # Create a notification for the user who owns the requested skill
        Notification.objects.create(
            user=skill.user,
            message=f"{request.user.username} has requested to trade {offered_skill.skill_name} for {skill.skill_name}."
        )

        # Redirect to the trade list after successful trade creation
        return redirect('trade_list')

    return render(request, 'initiate_trade.html', {
        'user_skills': user_skills,
        'available_skills': available_skills_to_trade,
        'preselected_skill': preselected_skill
    })



@login_required
def trade_list(request):
    trades = SkillTrade.objects.filter(requested_by=request.user)  # Fetch all trades for the logged-in user
    return render(request, 'trade_list.html', {'trades': trades})

@login_required
def accept_trade(request, trade_id):
    trade = get_object_or_404(SkillTrade, id=trade_id)
    trade.status = 'accepted'
    trade.save()
    return redirect('trade_list')

@login_required
def decline_trade(request, trade_id):
    trade = get_object_or_404(SkillTrade, id=trade_id)
    trade.status = 'declined'
    trade.save()
    return redirect('trade_list')





# views.py
@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    
    # Mark notifications as viewed
    for notification in notifications:
        notification.is_viewed = True
        notification.save()
        
    return render(request, 'accounts/notifications.html', {'notifications': notifications})



@login_required
def home(request):
    return render(request, 'accounts/home.html')




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message
from .forms import MessageForm

@login_required
def send_message(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        if user_id:
            # Redirect to the actual message sending page with the selected user
            return redirect('send_message_detail', user_id=user_id)
        else:
            # If no user selected, redirect back to message history
            return redirect('message_history')

    # Handle the POST request to send the message here (if applicable)



@login_required
def message_history(request):
    messages = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).order_by('timestamp')

    # Group messages by user
    user_messages = {}
    for message in messages:
        user = message.receiver if message.sender == request.user else message.sender
        if user not in user_messages:
            user_messages[user] = []
        user_messages[user].append(message)

    return render(request, 'accounts/message_history.html', {'user_messages': user_messages})


@login_required
def send_message_detail(request, user_id):
    receiver = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        Message.objects.create(sender=request.user, receiver=receiver, content=content)
        return redirect('message_history')  # Redirect back to message history after sending

    return render(request, 'accounts/send_message.html', {'receiver': receiver})


