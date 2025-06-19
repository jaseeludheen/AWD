from django.apps import apps


def get_all_custom_models():
    default_model = ['LogEntry', 'Permission', 'Group', 'ContentType', 'Session', 'User' ]

    # try to get all models 
    custom_models = []
    for model in apps.get_models():

        if model.__name__ not in default_model:
            custom_models.append(model.__name__)

    return custom_models

#        print(model.__name__)    # list of all models