from rest_framework.serializers import ValidationError


def validate_video_url(value):
    """Валидатор исключения запрещенных сайтов."""
    if "youtube.com" not in value.lower():
        raise ValidationError(
            "Cсылки на сторонние образовательные платформы или личные сайты — запрещены!"
        )
