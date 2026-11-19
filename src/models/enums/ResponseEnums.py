from enum import Enum

class ResponseSignal(str, Enum):
        
        file_validated_success = "File validated successfully."
        file_type_supported = "File type is supported."
        file_size_exceeded = "File size exceeds the allowed limit."
        file_upload_success = "File uploaded successfully."
        file_upload_failed = "File upload failed."
        file_valid = "File is valid."
        SUCCESS = "Success"

