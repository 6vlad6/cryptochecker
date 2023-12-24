from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from authentication.forms import CustomUserUpdateForm, CustomUserCreationForm, CustomUserRegistrationForm


def registrationView(request):
    if request.user.is_authenticated:
        return redirect('edit')
    else:
        messageError = ''
        if request.method == 'POST':
            form = CustomUserRegistrationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password1'])
                user.save()
                login(request, user)
                return redirect('home')
        else:
            form = CustomUserRegistrationForm()

        return render(request, 'registration.html', {'form': form})

def loginView(request):
    if request.user.is_authenticated:
        return redirect('edit')
    else:
        messageError = ''
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('edit')
                else:
                    messages.error('Имя пользователя или пароль неверны')
                    return redirect('auth')
        else:
            form = AuthenticationForm()

        return render(request, 'login.html', {'form': form})


def editView(request):
    if not request.user.is_authenticated:
        return redirect('home')
    else:
        if not request.user.is_authenticated:
            return redirect('auth')
        else:
            if request.method == 'POST':
                customUserForm = CustomUserUpdateForm(request.POST, request.FILES, instance=request.user)

                if customUserForm.is_valid():
                    customUserForm.save()
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                customUserForm = CustomUserUpdateForm()

            return render(request, 'edit.html', {'customUserForm': customUserForm})


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):

    template_name = 'change-password.html'
    success_message = "Пароль успешно сменен!"
    success_url = reverse_lazy('home')


def deleteAvatar(request):
    if not request.user.is_authenticated:
        return redirect('home')
    else:
        if request.user.img:
            request.user.img.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def logoutView(request):
    if not request.user.is_authenticated:
        return redirect('home')
    else:
        logout(request)

        return redirect('home')
