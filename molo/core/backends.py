from django.contrib.auth.models import Group
from django_cas_ng.backends import CASBackend
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class MoloCASBackend(CASBackend):

    def authenticate(self, request, ticket, service):
        user = super(
            MoloCASBackend, self).authenticate(request, ticket, service)
        if user is None:
            return None

        if 'attributes' in request.session \
            and 'has_perm' in request.session['attributes']\
                and request.session['attributes']['has_perm'] == 'True':
            if request.session['attributes']['is_admin'] == 'True':
                user.email = request.session['attributes']['email']
                user.is_staff = True
                user.is_superuser = True
                user.save()
            else:
                wagtail_login_only_group = Group.objects.filter(
                    name='Wagtail Login Only').first()
                if wagtail_login_only_group and not user.groups.exists():
                    user.groups.add(wagtail_login_only_group)

                elif not user.profile.admin_sites.filter(
                        pk=request.site.pk).exists():
                    return None

                """
                TODO: Handle case where Moderator group does not exist.
                We need to log this or find ways of notifying users that
                the moderator group was removed or renamed.
                There isn't much we can do about this case though.
                """
        else:
            user.is_staff = False
            user.is_superuser = False
            user.save()
            return None

        return user
