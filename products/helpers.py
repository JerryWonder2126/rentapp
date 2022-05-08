def get_upload_path(instance, filename):
    
    model = instance.album.model.__class__.meta
    name = model.verbose_name_plural.replace(' ', '_')

    return f"{name}/images/{filename}"