from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404

from viewer.forms import SecurityAnswerForm, SetNewPasswordForm
from viewer.models import User


def password_reset_step_1(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            request.session['reset_user_id'] = user.id
            return redirect('password_reset_step_2')
        except User.DoesNotExist:
            return render(request, 'reset_password/password_reset_step_1.html', {'error': 'Uživatel nebyl nalezen'})
    return render(request, 'reset_password/password_reset_step_1.html')


def password_reset_step_2(request):
    user_id = request.session.get('reset_user_id')
    if not user_id:
        return redirect('password_reset_step_1')
    user = get_object_or_404(User, id=user_id)
    profile = user.userprofile

    if request.method == 'POST':
        form = SecurityAnswerForm(request.POST)
        if form.is_valid():
            security_answer = form.cleaned_data['security_answer']
            if profile.check_security_answer(security_answer):
                return redirect('password_reset_step_3')
            else:
                error = 'Nesprávná odpověď nebo špatná otázka'
                return render(request, 'reset_password/password_reset_step_2.html', {'form': form, 'error': error, 'security_question': profile.security_question})
    else:
        form = SecurityAnswerForm()
    return render(request, 'reset_password/password_reset_step_2.html', {'form': form, 'security_question': profile.security_question})


def password_reset_step_3(request):
    user_id = request.session.get('reset_user_id')
    if not user_id:
        return redirect('password_reset_step_1')
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            new_password_confirm = form.cleaned_data['new_password_confirm']
            if new_password == new_password_confirm:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Vaše heslo bylo úspěšně změněno.')
                del request.session['reset_user_id']
                return redirect('login')
            else:
                form.add_error(None, 'Hesla se neshodují')
    else:
        form = SetNewPasswordForm()
    return render(request, 'reset_password/password_reset_step_3.html', {'form': form})