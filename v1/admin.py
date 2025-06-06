import os
import urllib.parse

from django.contrib import admin, messages
from django.contrib.admin.helpers import AdminForm
from django.contrib.admin.options import IS_POPUP_VAR
from django.contrib.admin.utils import unquote
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.admin import UserAdmin, sensitive_post_parameters_m
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils import timezone
from django.utils.html import escape
from django.utils.text import slugify
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from v1.models import Services, Errors, AllowedIP, AppSettings
from v1.models.service import TechnicalIssuePeriod, TechnicalIssuePeriodForm, TechnicalIssuePeriodTemplate
from v1.models.users import Partner
from .models import TelegramChat
from .models.allowed_ips import IP
from .utils.decorators import APP_LABEL
from v1.services.notification.telegram import notify


@admin.register(Partner)
class PartnerAdmin(UserAdmin):
    actions = ['download_credentials']
    list_display = 'id', 'username', 'identity', 'is_active', 'is_test', 'is_superuser', 'is_staff'
    list_display_links = 'id', 'username'
    list_editable = ['identity', 'is_active']
    fieldsets = (
        ("Partner Credentials",
         {"fields": ("username", "password", "secret", "identity", 'chats')}),
        (_("Permissions"),
         {"fields": ("is_active", "is_test", "is_staff", "is_superuser", "groups", "user_permissions")})
    )

    @sensitive_post_parameters_m
    def user_change_password(self, request, id, form_url=""):
        user = self.get_object(request, unquote(id))
        if not self.has_change_permission(request, user):
            raise PermissionDenied
        if user is None:
            raise Http404(
                _("%(name)s object with primary key %(key)r does not exist.")
                % {
                    "name": self.opts.verbose_name,
                    "key": escape(id),
                }
            )
        if request.method == "POST":
            form = self.change_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                change_message = self.construct_change_message(request, form, None)
                self.log_change(request, user, change_message)
                msg = gettext("Password changed successfully.")
                messages.success(request, f'File password is: {user._file_password}')
                messages.success(request, msg)
                update_session_auth_hash(request, form.user)
                return HttpResponseRedirect(
                    reverse(
                        "%s:%s_%s_change"
                        % (
                            self.admin_site.name,
                            user._meta.app_label,
                            user._meta.model_name,
                        ),
                        args=(user.pk,),
                    )
                )
        else:
            form = self.change_password_form(user)

        fieldsets = [(None, {"fields": list(form.base_fields)})]
        admin_form = AdminForm(form, fieldsets, {})

        context = {
            "title": _("Change password: %s") % escape(user.get_username()),
            "adminForm": admin_form,
            "form_url": form_url,
            "form": form,
            "is_popup": (IS_POPUP_VAR in request.POST or IS_POPUP_VAR in request.GET),
            "is_popup_var": IS_POPUP_VAR,
            "add": True,
            "change": False,
            "has_delete_permission": False,
            "has_change_permission": True,
            "has_absolute_url": False,
            "opts": self.opts,
            "original": user,
            "save_as": False,
            "show_save": True,
            **self.admin_site.each_context(request),
        }

        request.current_app = self.admin_site.name

        return TemplateResponse(
            request,
            self.change_user_password_template
            or "admin/auth/user/change_password.html",
            context,
        )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.set_password(form.cleaned_data['password'])  # Assuming 'password' is the field name in your form
            obj.save()  # Save the object to generate the file password
            self.message_user(request, f'File password is: {obj._file_password}')
        result = super().save_model(request, obj, form, change)
        return result

    def download_credentials(self, request, queryset):
        if queryset.count() == 1:
            user = queryset.first()
            # Serve the protected zip file as a response
            with open(user.path_to_protected_zip, 'rb') as zip_file_protected:
                response = HttpResponse(zip_file_protected.read(), content_type='application/zip')
                response['Content-Disposition'] = f'attachment; filename="{slugify(user.username)}_secret.zip"'
                response['Content-Length'] = os.path.getsize(user.path_to_protected_zip)
                return response
        self.message_user(request, 'Please select only one user for this action.')


@admin.register(Services)
class ServicesAdminModel(admin.ModelAdmin):
    list_display = [field.name for field in Services._meta.fields]

    def save_model(self, request, obj, form, change):
        # Save the service
        super().save_model(request, obj, form, change)

        # Create a permission for the service
        codename = f"{obj.method_name.lower()}"
        name = f"{obj.method_name}"

        # Get the content type of the desired model associated with the view
        permission = Permission.objects.filter(codename=codename).first()

        # Create the permission associated with the app
        c_t = ContentType.objects.filter(app_label=APP_LABEL).first()
        if not permission:
            Permission.objects.create(codename=codename, name=name,
                                      content_type=c_t)

        # Create permissions based on the is_crud field
        if obj.is_crud:
            codename = obj.method_name.lower()
            permissions = [
                ('create', f"Can create {obj.method_name}"),
                ('view', f"Can view {obj.method_name}"),
                ('update', f"Can update {obj.method_name}"),
                ('delete', f"Can delete {obj.method_name}")
            ]

            for perm in permissions:
                perm_codename = f'{codename}.{perm[0]}'
                permission = Permission.objects.filter(codename=perm_codename, content_type=c_t).first()
                if not permission:
                    Permission.objects.create(codename=perm_codename, name=perm[1], content_type=c_t)


class TechnicalIssuePeriodAdmin(admin.ModelAdmin):
    form = TechnicalIssuePeriodForm
    list_display = ['service', 'duration', 'start_timestamp', 'end_timestamp']
    fields = ['service', 'duration', 'template', 'notify', 'start_timestamp']

    def save_model(self, request, obj, form, change):
        # Get start time
        obj.start_timestamp = timezone.now()

        # Get duration in minutes
        duration = obj.duration

        # calculate end_timestamp
        obj.end_timestamp = obj.start_timestamp + timezone.timedelta(minutes=duration)

        # Create TIP
        obj.save()

        # Set Service status to TEMPORARILY
        # TODO: in case of not recent  start_timestamp do further changes
        service = obj.service
        service.status = Services.StatusType.TEMPORARILY.value
        service.save()
        if obj.notify:
            if obj.template is not None:

                date = obj.start_timestamp.strftime('%Y-%m-%d')
                start_time = obj.start_timestamp.strftime('%H:%M')
                end_time = obj.end_timestamp.strftime('%H:%M')

                tag = urllib.parse.quote(obj.template.tag)
                msg = f'<b>{obj.template.title}</b>\n' \
                      f'<pre>-------------------------</pre>\n' \
                      f'🇺🇿 {obj.template.uz}\n' \
                      f'<pre>* * *</pre>\n' \
                      f'🇷🇺 {obj.template.ru}\n' \
                      f'<pre>* * *</pre>\n' \
                      f'🇬🇧 {obj.template.en}\n' \
                      f'<pre>-------------------------</pre>' \
                      f'<pre>{tag}</pre>'

                replacements = {
                    'duration': f'<b>{duration}</b>',
                    'service_name': f'<b>{service.method_name}</b>',
                    'date': f'<b>{date}</b>',
                    'start_time': f'<b>{start_time}</b>',
                    'end_time': f'<b>{end_time}</b>',
                }

                for key, value in replacements.items():
                    msg = msg.replace(key, value)
            else:
                # TODO: Later make more reliable notify method
                msg = f'🚨🚨 {service} 🚨🚨\n' \
                      f'🕧 For {duration} minutes\n' \
                      f'Start time: <pre>{obj.start_timestamp}</pre>\n' \
                      f'End time: <pre>{obj.end_timestamp}</pre>'

            notify(msg=msg, mode='all')


admin.site.register(TechnicalIssuePeriod, TechnicalIssuePeriodAdmin)


@admin.register(TechnicalIssuePeriodTemplate)
class TechnicalIssuePeriodTemplateAdminModel(admin.ModelAdmin):
    # Display all related columns in case of TIP
    list_display = [field.name for field in TechnicalIssuePeriodTemplate._meta.fields]


@admin.register(Errors)
class ErrorAdminModel(admin.ModelAdmin):
    # Error messages DB
    list_display = [field.name for field in Errors._meta.fields]


class TelegramChatAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TelegramChat._meta.fields]
    search_fields = ('name', 'username')
    actions = ['get_updates_action']

    change_list_template = 'telegram_get_updates_change_list.html'


admin.site.register(TelegramChat, TelegramChatAdmin)


@admin.register(AllowedIP)
class AllowedIPAdminModel(admin.ModelAdmin):
    # Error messages DB
    list_display = [field.name for field in AllowedIP._meta.fields]


@admin.register(IP)
class IPAdminModel(admin.ModelAdmin):
    # Error messages DB
    list_display = [field.name for field in IP._meta.fields]


@admin.register(AppSettings)
class AppSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not AppSettings.objects.exists()  # Only allow one

    def has_delete_permission(self, request, obj=None):
        return False  # Prevent deletion
