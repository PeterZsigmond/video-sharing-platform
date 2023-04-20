from fastapi import UploadFile, status, HTTPException


def validate_upload_file_type(file: UploadFile, valid_types: list[str]):
    if file.content_type is None or file.content_type not in valid_types:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail={"Allowed content types:": valid_types})


def validate_upload_file_size(file: UploadFile, mb: int):
    if file.size is None or file.size == 0 or file.size > (mb * 1024 * 1024):
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="Allowed maximum file size: " + str(mb) + "MB.")


def write_file(file: UploadFile, file_path: str):
    with open(file_path, 'wb') as f:
        f.write(file.file.read())
