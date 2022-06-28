from django.contrib.auth.backends import RemoteUserBackend, ModelBackend
from django.contrib.auth import get_user_model
User = get_user_model()

'''

    The CustomModelBackend allows for overriding the query that is run on 
    each page request to get the authenticated user (request.user in the 
    view or {{ user }} on a template). This can be useful for selecting or
    prefetching related data to prevent additional queries on each request.

    In settings.py, replace this line:
        'django.contrib.auth.backends.ModelBackend'

    with this one:
        'project.auth.backends.CustomModelBackend'

'''



class CustomModelBackend(ModelBackend):
    def get_user(self, user_id):
        try:
            return User.objects\
                .prefetch_related('groups')\
                .get(pk=user_id)

        except User.DoesNotExist:
            return None

        except Exception as e:
            return None
