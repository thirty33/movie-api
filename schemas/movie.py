from pydantic import BaseModel, Field

class Movie(BaseModel):
    # id: Optional[int]
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=2022)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=5, max_length=15)

    class Config:
        json_schema_extra = {
            "example": {
                # "id": 1,
                "title": "Movie title",
                "overview": "Movie description",
                "year": 2022,
                "rating": 9.8,
                "category": "Acción"
            }
        }