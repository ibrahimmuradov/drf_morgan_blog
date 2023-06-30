
class Uploader:
    @staticmethod
    def upload_image_blog(objName, filename):
        return f"image/{objName.blog.slug}/{filename}"

    @staticmethod
    def upload_profile_photo(objName, filename):
        return f"image/{objName.username}/{filename}"
