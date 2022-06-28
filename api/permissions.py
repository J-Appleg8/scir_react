from rest_framework.permissions import DjangoModelPermissions
import copy

class DefaultPermissions(DjangoModelPermissions):
    def __init__(self):
        '''
        By default, anyone is allowed to view models. This changes 
        it to follow the Django `view_model_name` permissions for
        the model.
        '''
        
        self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']
