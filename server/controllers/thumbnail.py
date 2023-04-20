from os import path
from fastapi import HTTPException, status


def get_thumbnail_path(id: int):
    return "videos/" + str(id) + ".png"


def validate_thumbnail_exists(thumbnail_path: str):
    if not path.isfile(thumbnail_path):
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
