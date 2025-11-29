from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image

def resize_image(file, max_width=1080):
    img = Image.open(file)
    
    if img.width <= max_width:
        return img
    
    ratio = max_width / img.width
    new_height = ratio * img.height
    
    img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)    
    buffer = BytesIO()    
    img.save(buffer, format='JPEG', quality=75)
    buffer.seek(0)

    return ContentFile(buffer.read(), name=file.name)