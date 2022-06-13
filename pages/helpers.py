from products.models import ImageAlbum


def create_album(images, album_hash=None):
    """ Creates a new image album and returns it. Delete album identified by album_hash if given """
    if album_hash:
        ImageAlbum.objects.delete(album_hash=album_hash)
    album = ImageAlbum()
    album.save(images)
    return album