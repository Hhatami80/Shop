import os
from utils.image_hash import get_image_hash


class DedupImageMixin:
    image_field_name = 'image'

    def create(self, validated_data):
        image_file = validated_data.get(self.image_field_name)
        if not image_file:
            return super().create(validated_data)

        image_hash = get_image_hash(image_file)

        model_class = getattr(self.Meta, 'model', None)
        if not model_class:
            raise AssertionError("Meta.model must be defined.")

        existing = model_class.objects.filter(image_hash=image_hash).first()
        if existing:
            if existing.image and hasattr(existing.image, 'path') and os.path.isfile(existing.image.path):
                os.remove(existing.image.path)
            existing.delete()

        validated_data['image_hash'] = image_hash
        return super().create(validated_data)
