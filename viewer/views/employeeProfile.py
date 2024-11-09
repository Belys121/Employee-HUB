from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect

from viewer.forms import EmployeeInformationForm, BankAccountForm, EmergencyContactForm, BaseEmergencyContactFormSet, \
    SecurityQuestionForm
from viewer.models import UserProfile, EmployeeInformation, BankAccount, EmergencyContact
from viewer.views.utils import logger



@login_required
def employee_profile(request):
    """
    Displays and manages the employee profile page and allows users to view and edit information
        about the employee, bank account details and emergency contacts.
    Handles both GET and POST requests with enhanced error handling:
        - GET: Retrieves and displays user profile information with edit forms for various sections.
        - POST: Processes form submissions for employee, bank account or emergency contact information.
    Enhanced error handling search exception logging and user notification of problems and redirection back
        to the profile page if errors occur.
    """
    user = request.user

    try:
        user_profile, created = UserProfile.objects.get_or_create(user=user)
    except Exception as e:
        logger.error(f"Error fetching/creating UserProfile for user {user.id}: {e}")
        messages.error(request, 'An error occurred while fetching your profile. Please try again later.')
        return redirect('home')

    edit_section = request.GET.get('edit')

    # Inicializing form like None
    bank_account_form = None
    employee_information_form = None
    emergency_contact_formset = None

    # Processing POST requests
    if request.method == 'POST':
        if 'employee_information_submit' in request.POST:
            try:
                employee_information = user_profile.employeeinformation
            except EmployeeInformation.DoesNotExist:
                employee_information = None
            employee_information_form = EmployeeInformationForm(request.POST, instance=employee_information)

            if employee_information_form.is_valid():
                try:
                    employee_information = employee_information_form.save(commit=False)
                    employee_information.user_profile = user_profile
                    employee_information.save()
                    messages.success(request, 'Informace o zaměstnanci úspěšně upraveny.')
                    return redirect('employee_profile')
                except Exception as e:
                    logger.error(f"Error saving EmployeeInformation for user {user.id}: {e}")
                    messages.error(request, 'An error occurred while saving employee information.')
            else:
                messages.error(request, 'Opravte prosím níže uvedené chyby.')

        elif 'bank_account_submit' in request.POST:
            try:
                bank_account = user_profile.bankaccount
            except BankAccount.DoesNotExist:
                bank_account = None
            bank_account_form = BankAccountForm(request.POST, instance=bank_account)

            if bank_account_form.is_valid():
                try:
                    bank_account = bank_account_form.save(commit=False)
                    bank_account.user_profile = user_profile
                    bank_account.save()
                    messages.success(request, 'Bankovní údaje úspěšně upraveny.')
                    return redirect('employee_profile')
                except Exception as e:
                    logger.error(f"Error saving BankAccount for user {user.id}: {e}")
                    messages.error(request, 'An error occurred while saving bank account details.')
            else:
                messages.error(request, 'Opravte prosím níže uvedené chyby.')

        elif 'emergency_contact_submit' in request.POST:
            EmergencyContactFormSetAdjusted = inlineformset_factory(
                UserProfile,
                EmergencyContact,
                form=EmergencyContactForm,
                formset=BaseEmergencyContactFormSet,
                extra=1,
                max_num=2,
                can_delete=True,
            )
            emergency_contact_formset = EmergencyContactFormSetAdjusted(request.POST, instance=user_profile)

            if emergency_contact_formset.is_valid():
                try:
                    emergency_contact_formset.save()
                    messages.success(request, 'Kontaktní osoby úspěšně upraveny.')
                    return redirect('employee_profile')
                except Exception as e:
                    logger.error(f"Error saving EmergencyContact for user {user.id}: {e}")
                    messages.error(request, 'An error occurred while updating emergency contacts.')
            else:
                messages.error(request, 'Opravte prosím níže uvedené chyby.')

    # Processing GET requests
    else:
        if edit_section == 'information':
            try:
                employee_information = user_profile.employeeinformation
            except EmployeeInformation.DoesNotExist:
                employee_information = None
            employee_information_form = EmployeeInformationForm(instance=employee_information)

        elif edit_section == 'account':
            try:
                bank_account = user_profile.bankaccount
            except BankAccount.DoesNotExist:
                bank_account = None
            bank_account_form = BankAccountForm(instance=bank_account)

        elif edit_section == 'emergency_contacts':
            EmergencyContactFormSetAdjusted = inlineformset_factory(
                UserProfile,
                EmergencyContact,
                form=EmergencyContactForm,
                formset=BaseEmergencyContactFormSet,
                extra=1 if user_profile.emergency_contacts.count() == 0 else 0,
                max_num=2,
                can_delete=True,
            )
            emergency_contact_formset = EmergencyContactFormSetAdjusted(instance=user_profile)

    # Getting data only for read
    try:
        employee_information = user_profile.employeeinformation
    except EmployeeInformation.DoesNotExist:
        employee_information = None

    try:
        bank_account = user_profile.bankaccount
    except BankAccount.DoesNotExist:
        bank_account = None

    context = {
        'user': user,
        'user_profile': user_profile,
        'employee_information_form': employee_information_form,
        'bank_account_form': bank_account_form,
        'emergency_contact_formset': emergency_contact_formset,
        'employee_information': employee_information,
        'bank_account': bank_account,
    }

    return render(request, 'other/employee_profile.html', context)


@login_required
def change_security_question_view(request):
    user_profile = request.user.userprofile
    if request.method == 'POST':
        form = SecurityQuestionForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bezpečnostní otázka a odpověď byly úspěšně změněny.')
            return redirect('employee_profile')
    else:
        form = SecurityQuestionForm(instance=user_profile)
    return render(request, 'forms/form.html', {'form': form})
