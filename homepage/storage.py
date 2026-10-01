from django.core.files.storage import storages


def get_r2_storage():
    return storages["r2"]