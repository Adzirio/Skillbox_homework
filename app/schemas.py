from pydantic import BaseModel, ConfigDict


class RecipeCreate(BaseModel):
    title: str
    cooking_time: int
    ingredients: str
    description: str


class RecipeList(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    views: int
    cooking_time: int


class RecipeDetail(RecipeList):
    ingredients: str
    description: str
