from pathlib import Path

import magic
from django.utils.deconstruct import deconstructible

import re
from django.core.exceptions import (
    FieldDoesNotExist, ValidationError,
)
from difflib import SequenceMatcher
from django.utils.translation import gettext as _



@deconstructible
class DocumentFileMimeValidator:
    """
    Validator PDF files using pdf type
    """
    messages = {
        "malicious_file": "File looks malicious. Allowed extensions are: '%(allowed_extensions)s'.",
        "not_supported": "File extension '%(extension)s' is not allowed. Allowed extensions are: '%(allowed_extensions)s'.", 
        "wrong_size": "File size not correct. Allowed file size are min = 1 kb max = 512kb."
    }
    code = 'invalid_extension'
    ext_cnt_mapping = {
        'pdf': 'application/pdf',
    }

    file_size_lower_bound = 1024  # 1024 bytes
    file_size_upper_bound = 512 * 1024  # 2 mega bytes

    allowed_extensions = [allowed_extension.lower() for allowed_extension in ext_cnt_mapping.keys()]

    def __call__(self, data):
        # validate file size
        file_size = data.size
        if file_size < self.file_size_lower_bound or file_size > self.file_size_upper_bound:
            raise ValidationError(
                self.messages['wrong_size'],
                code = self.code,
                params={}
            )
        # validate file extension
        extension = Path(data.name).suffix[1:].lower()
        content_type = magic.from_buffer(data.read(1024), mime=True)
        if extension not in self.allowed_extensions:
            raise ValidationError(
                self.messages['not_supported'],
                code=self.code,
                params={
                    'extension': extension,
                    'allowed_extensions': ', '.join(self.allowed_extensions)
                }
            )
        if content_type != self.ext_cnt_mapping[extension]:
            raise ValidationError(
                self.messages['malicious_file'],
                code=self.code,
                params={
                    'allowed_extensions': ', '.join(self.allowed_extensions)
                }
            )

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.allowed_extensions == other.allowed_extensions and
            self.message == other.message and
            self.code == other.code
        )



class UserNameSimilarityValidator:
    """
    Validate whether the password is sufficiently different from the user's
    user_name.

    If no specific attributes are provided, look at a sensible list of
    defaults. Attributes that don't exist are ignored. Comparison is made to
    not only the full attribute value, but also its components, so that, for
    example, a password is validated against either part of an email address,
    as well as the full address.
    """
    DEFAULT_USER_ATTRIBUTES = ('user_name',)

    def __init__(self, user_attributes=DEFAULT_USER_ATTRIBUTES, max_similarity=0.7):
        self.user_attributes = user_attributes
        self.max_similarity = max_similarity

    def validate(self, password, user=None):
        if not user:
            return

        for attribute_name in self.user_attributes:
            value = user.user_name
            if not value or not isinstance(value, str):
                continue
            value_parts = re.split(r'\W+', value) + [value]
            for value_part in value_parts:
                if SequenceMatcher(a=password.lower(), b=value_part.lower()).quick_ratio() >= self.max_similarity:
                    try:
                        verbose_name = str(user._meta.get_field(attribute_name).verbose_name)
                    except FieldDoesNotExist:
                        verbose_name = attribute_name
                    raise ValidationError(
                        _("The password is too similar to the %(verbose_name)s."),
                        code='password_too_similar',
                        params={'verbose_name': verbose_name},
                    )

    def get_help_text(self):
        return _("Your password can't be too similar to your other personal information.")