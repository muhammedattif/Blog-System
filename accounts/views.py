from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import CreationUserForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from django.conf import settings
from django.contrib.auth.models import User
# Create your views here.

def signin(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                if 'next' in request.GET: # this line used to redirect the user to the link he clicked on before login
                    return redirect(request.GET.get('next'))
                else:
                    return redirect('/')
            else:
                messages.info(request, "invalid cradentials")
                return redirect('/accounts/signin')

        else:
            return render(request, 'login.html')
    else:
        return redirect('/')


def register(request):
    form = CreationUserForm()

    if request.method == "POST":
        form = CreationUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for {}'.format(user))
            return redirect('/accounts/signin')
        else:
            messages.error(request, 'Form is not valid.')

    context = {
      'form': form
    }
    return render(request, 'register.html', context)

# @login_required means that user must be logedin to access this function
@login_required(login_url='/accounts/signin')
def signout(request):
    logout(request)
    return redirect('/accounts/signin')

# Class-Based-View example
class UpdateProfile(UpdateView):
    template_name = 'Update_profile.html'
    form_class = CreationUserForm
    success_url = '/'
    success_message = "Profile Updated successfully"

    def get_object(self):
        return get_object_or_404(User, pk = self.request.user.pk)

    def form_invalid(self, form):
        return super().form_invalid(form)


    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
