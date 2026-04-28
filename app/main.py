from contextlib import asynccontextmanager
from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import engine, get_db, init_db
from app.models import Recipe
from app.schemas import RecipeCreate, RecipeDetail, RecipeList


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await engine.dispose()


app = FastAPI(
    title="Кулинарная книга API (Async)",
    version="1.1.0",
    lifespan=lifespan,
)


@app.get("/recipes", response_model=List[RecipeList])
async def get_recipes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Recipe).order_by(
            Recipe.views.desc(),
            Recipe.cooking_time.asc(),
        )
    )
    return result.scalars().all()


@app.get("/recipes/{recipe_id}", response_model=RecipeDetail)
async def get_recipe(recipe_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Recipe).where(Recipe.id == recipe_id))
    recipe = result.scalars().first()

    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Рецепт не найден",
        )

    await db.execute(
        update(Recipe).where(Recipe.id == recipe_id).values(views=Recipe.views + 1)
    )
    await db.commit()
    await db.refresh(recipe)
    return recipe


@app.post("/recipes", response_model=RecipeDetail, status_code=status.HTTP_201_CREATED)
async def create_recipe(
    recipe: RecipeCreate,
    db: AsyncSession = Depends(get_db),
):
    db_recipe = Recipe(**recipe.model_dump())
    db.add(db_recipe)
    await db.commit()
    await db.refresh(db_recipe)
    return db_recipe
