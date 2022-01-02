from pydantic import BaseModel


class SearchImagesRequest(BaseModel):
    data: str
    max_num_hits: int
