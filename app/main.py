from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

app = FastAPI(title="Recipe App API")

Base = declarative_base()

# User model for login/authentication
class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    recipes = relationship("Recipe", back_populates="user", cascade="all, delete")
    favorites = relationship("UserFavorite", back_populates="user", cascade="all, delete")


# Recipe model (ingredients as a field)
class Recipe(Base):
    __tablename__ = "recipes"
    recipe_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    instructions = Column(Text)
    ingredients = Column(Text, nullable=False)  # JSON or comma-separated list
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="recipes")
    favorited_by = relationship("UserFavorite", back_populates="recipe", cascade="all, delete")

# User favorites
class UserFavorite(Base):
    __tablename__ = "user_favorites"
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    recipe_id = Column(Integer, ForeignKey("recipes.recipe_id", ondelete="CASCADE"), primary_key=True)
    favorited_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="favorites")
    recipe = relationship("Recipe", back_populates="favorited_by")




# Robust absolute path for recipes.db in artifacts folder
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, '../artifacts/recipes.db')}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=False
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# Dependency for FastAPI endpoints
def get_db():
    """
    Provides a database session for FastAPI dependency injection.
    
    This function is a generator that creates a new SQLAlchemy database session
    for each request and ensures it's properly closed after the request completes.
    It's designed to be used as a dependency in FastAPI route handlers to manage
    database connections efficiently.
    
    Args:
        None
    
    Yields:
        Session: A SQLAlchemy database session instance that can be used to
            query and modify the database. The session is automatically committed
            or rolled back based on the success of the request.
    
    Raises:
        None: This function doesn't raise exceptions directly, but database
            operations using the yielded session may raise SQLAlchemy exceptions.
    
    Notes:
        - Uses the SessionLocal factory configured with the SQLite database
        - Implements the context manager pattern with try/finally
        - Ensures database connections are closed even if exceptions occur
        - Thread-safe for SQLite with check_same_thread=False
        - Used with FastAPI's Depends() for automatic dependency injection
    
    Example:
        >>> @app.get("/items/")
        ... def read_items(db: Session = Depends(get_db)):
        ...     return db.query(Item).all()
    
    Dependencies:
        - SessionLocal: SQLAlchemy session factory
        - Session: SQLAlchemy session class
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# ---------------------- #
# Pydantic MODELS        #
# ---------------------- #

class UserBase(BaseModel):
    username: str = Field(..., min_length=1, max_length=64)
    email: EmailStr
    password_hash: str = Field(..., min_length=1, max_length=128)

class UserCreate(UserBase):
    pass

class UserResponse(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True


class IngredientEntry(BaseModel):
    name: str
    quantity: str


class RecipeBase(BaseModel):
    title: str
    description: Optional[str] = None
    instructions: Optional[str] = None
    ingredients: List[IngredientEntry]

class RecipeCreate(RecipeBase):
    pass


class RecipeResponse(BaseModel):
    recipe_id: int
    user_id: int
    title: str
    description: Optional[str]
    instructions: Optional[str]
    created_at: datetime
    ingredients: List[IngredientEntry]
    class Config:
        orm_mode = True


# ---------------------- #
# ENDPOINTS              #
# ---------------------- #


from fastapi import Depends

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first()

def get_recipe_by_id(db: Session, recipe_id: int):
    return db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()

def get_ingredient_by_id(db: Session, ingredient_id: int):
    return db.query(Ingredient).filter(Ingredient.ingredient_id == ingredient_id).first()

# User endpoints
@app.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    if get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=user.password_hash,
        created_at=datetime.utcnow()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/", response_model=List[UserResponse])
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return None




# Recipe endpoints
import json
@app.post("/recipes/", response_model=RecipeResponse, status_code=status.HTTP_201_CREATED)
def create_recipe(recipe: RecipeCreate, db: Session = Depends(get_db)):
    # For demo, assign to user_id=1 (should be from auth in real app)
    db_recipe = Recipe(
        user_id=1,
        title=recipe.title,
        description=recipe.description,
        instructions=recipe.instructions,
        ingredients=json.dumps([ing.dict() for ing in recipe.ingredients]),
        created_at=datetime.utcnow()
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return RecipeResponse(
        recipe_id=db_recipe.recipe_id,
        user_id=db_recipe.user_id,
        title=db_recipe.title,
        description=db_recipe.description,
        instructions=db_recipe.instructions,
        created_at=db_recipe.created_at,
        ingredients=recipe.ingredients
    )


@app.get("/recipes/", response_model=List[RecipeResponse])
def list_recipes(db: Session = Depends(get_db)):
    recipes = db.query(Recipe).all()
    result = []
    for r in recipes:
        try:
            ingredients = [IngredientEntry(**ing) for ing in json.loads(r.ingredients)]
        except Exception:
            ingredients = []
        result.append(RecipeResponse(
            recipe_id=r.recipe_id,
            user_id=r.user_id,
            title=r.title,
            description=r.description,
            instructions=r.instructions,
            created_at=r.created_at,
            ingredients=ingredients
        ))
    return result


@app.get("/recipes/{recipe_id}", response_model=RecipeResponse)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    r = get_recipe_by_id(db, recipe_id)
    if not r:
        raise HTTPException(status_code=404, detail="Recipe not found")
    try:
        ingredients = [IngredientEntry(**ing) for ing in json.loads(r.ingredients)]
    except Exception:
        ingredients = []
    return RecipeResponse(
        recipe_id=r.recipe_id,
        user_id=r.user_id,
        title=r.title,
        description=r.description,
        instructions=r.instructions,
        created_at=r.created_at,
        ingredients=ingredients
    )

# User favorites endpoints
@app.post("/users/{user_id}/favorites/{recipe_id}", status_code=status.HTTP_201_CREATED)
def add_favorite(user_id: int, recipe_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    recipe = get_recipe_by_id(db, recipe_id)
    if not user or not recipe:
        raise HTTPException(status_code=404, detail="User or Recipe not found")
    fav = db.query(UserFavorite).filter_by(user_id=user_id, recipe_id=recipe_id).first()
    if fav:
        raise HTTPException(status_code=400, detail="Already favorited")
    db.add(UserFavorite(user_id=user_id, recipe_id=recipe_id))
    db.commit()
    return {"message": "Recipe favorited"}

@app.get("/users/{user_id}/favorites/", response_model=List[RecipeResponse])
def list_favorites(user_id: int, db: Session = Depends(get_db)):
    favs = db.query(UserFavorite).filter_by(user_id=user_id).all()
    recipes = [get_recipe_by_id(db, fav.recipe_id) for fav in favs]
    result = []
    import json
    for r in recipes:
        if r:
            try:
                ingredients = [IngredientEntry(**ing) for ing in json.loads(r.ingredients)]
            except Exception:
                ingredients = []
            result.append(RecipeResponse(
                recipe_id=r.recipe_id,
                user_id=r.user_id,
                title=r.title,
                description=r.description,
                instructions=r.instructions,
                created_at=r.created_at,
                ingredients=ingredients
            ))
    return result

# ---------------------- #
# To run:
# uvicorn main:app --reload
# ---------------------- #

# Export Base for testing
Base = Base

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)