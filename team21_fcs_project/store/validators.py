from pathlib import Path

import magic
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class ImageFileMimeValidator:
    """
    Validator PDF files using pdf type
    """
    messages = {
        "malicious_file": "File looks malicious. Allowed extensions are: '%(allowed_extensions)s'.",
        "not_supported": "File extension '%(extension)s' is not allowed. Allowed extensions are: '%(allowed_extensions)s'.", 
        "wrong_size": "File size not correct. Allowed file size are min = 1kb max = 512kb"
    }
    code = 'invalid_extension'
    ext_cnt_mapping = {
        'jpeg': 'image/jpeg',
        'png': 'image/png',
    }

    file_size_lower_bound = 1024  # 1024 bytes
    file_size_upper_bound = 512 * 1024  # 512 kilo bytes

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