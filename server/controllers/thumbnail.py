from os import path, remove
from fastapi import HTTPException, status, UploadFile
from server.controllers.file import validate_upload_file_type, validate_upload_file_size, write_file
from server.config import MAX_THUMBNAIL_SIZE_IN_MB


valid_image_types = ["image/png", "image/jpeg"]


def get_thumbnail_dir():
    return "videos/"


def get_thumbnail_path(id: int):
    for content_type in valid_image_types:
        file_path = thumbnail_file_path(id, content_type)
        if path.isfile(file_path):
            return file_path
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)


def validate_thumbnail_file(thumbnail: UploadFile):
    validate_upload_file_type(thumbnail, valid_image_types)
    validate_upload_file_size(thumbnail, MAX_THUMBNAIL_SIZE_IN_MB)
    return thumbnail


def delete_thumbnail(id: int):
    for content_type in valid_image_types:
        file_path = thumbnail_file_path(id, content_type)
        if path.isfile(file_path):
            remove(file_path)


def write_thumbnail_file(thumbnail: UploadFile, id: int):
    file_path = thumbnail_file_path(id, str(thumbnail.content_type))
    write_file(thumbnail, file_path)


def thumbnail_file_path(id: int, content_type: str):
    file_type = content_type.split("/")[1]
    file_path = get_thumbnail_dir() + str(id) + "." + file_type
    return file_path
