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
    Float,
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

app = FastAPI(title="Users CRUD API")

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    user_role = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    onboarding_checklists = relationship("UserOnboardingChecklist", back_populates="user", cascade="all, delete")
    resource_progress = relationship("UserResourceProgress", back_populates="user", cascade="all, delete")
    quiz_attempts = relationship("UserQuizAttempt", back_populates="user", cascade="all, delete")
    mentorships_as_mentor = relationship("Mentorship", back_populates="mentor", foreign_keys='Mentorship.mentor_id', cascade="all, delete")
    mentorships_as_mentee = relationship("Mentorship", back_populates="mentee", foreign_keys='Mentorship.mentee_id', cascade="all, delete")
    social_connections_requested = relationship("SocialConnection", back_populates="requester", foreign_keys='SocialConnection.requester_id', cascade="all, delete")
    social_connections_received = relationship("SocialConnection", back_populates="addressee", foreign_keys='SocialConnection.addressee_id', cascade="all, delete")

class OnboardingTask(Base):
    __tablename__ = "onboarding_tasks"

    task_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    category = Column(String)

    # Relationships
    user_checklists = relationship("UserOnboardingChecklist", back_populates="task", cascade="all, delete")

class UserOnboardingChecklist(Base):
    __tablename__ = "user_onboarding_checklists"

    checklist_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    task_id = Column(Integer, ForeignKey("onboarding_tasks.task_id", ondelete="CASCADE"), nullable=False)
    status = Column(String, nullable=False, default='pending')
    assigned_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)

    # Relationships
    user = relationship("User", back_populates="onboarding_checklists")
    task = relationship("OnboardingTask", back_populates="user_checklists")

class Resource(Base):
    __tablename__ = "resources"

    resource_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    resource_type = Column(String, nullable=False)
    content_url = Column(String)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user_progress = relationship("UserResourceProgress", back_populates="resource", cascade="all, delete")
    quizzes = relationship("Quiz", back_populates="resource", cascade="all, delete")

class UserResourceProgress(Base):
    __tablename__ = "user_resource_progress"

    progress_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    resource_id = Column(Integer, ForeignKey("resources.resource_id", ondelete="CASCADE"), nullable=False)
    status = Column(String, nullable=False, default='not_started')
    completed_at = Column(DateTime)
    last_accessed_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="resource_progress")
    resource = relationship("Resource", back_populates="user_progress")

class Quiz(Base):
    __tablename__ = "quizzes"

    quiz_id = Column(Integer, primary_key=True, autoincrement=True)
    resource_id = Column(Integer, ForeignKey("resources.resource_id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)

    # Relationships
    resource = relationship("Resource", back_populates="quizzes")
    attempts = relationship("UserQuizAttempt", back_populates="quiz", cascade="all, delete")

class UserQuizAttempt(Base):
    __tablename__ = "user_quiz_attempts"

    attempt_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    quiz_id = Column(Integer, ForeignKey("quizzes.quiz_id", ondelete="CASCADE"), nullable=False)
    score = Column(Float)
    feedback = Column(Text)
    attempted_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="quiz_attempts")
    quiz = relationship("Quiz", back_populates="attempts")

class Mentorship(Base):
    __tablename__ = "mentorships"

    mentorship_id = Column(Integer, primary_key=True, autoincrement=True)
    mentor_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    mentee_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    status = Column(String, nullable=False, default='pending')
    requested_at = Column(DateTime, default=datetime.utcnow)
    accepted_at = Column(DateTime)

    # Relationships
    mentor = relationship("User", foreign_keys=[mentor_id], back_populates="mentorships_as_mentor")
    mentee = relationship("User", foreign_keys=[mentee_id], back_populates="mentorships_as_mentee")

class SocialConnection(Base):
    __tablename__ = "social_connections"

    connection_id = Column(Integer, primary_key=True, autoincrement=True)
    requester_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    addressee_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    status = Column(String, nullable=False, default='pending')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime)

    # Relationships
    requester = relationship("User", foreign_keys=[requester_id], back_populates="social_connections_requested")
    addressee = relationship("User", foreign_keys=[addressee_id], back_populates="social_connections_received")



# Robust absolute path for onboarding.db in artifacts folder
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, '../artifacts/onboarding.db')}"

# echo=True for debugging; set to False in production

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=False
)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables if they do not exist
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
    full_name: str = Field(..., min_length=1, max_length=128)
    email: EmailStr
    user_role: str = Field(..., min_length=1, max_length=64)

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=1, max_length=128)
    email: Optional[EmailStr] = None
    user_role: Optional[str] = Field(None, min_length=1, max_length=64)

class UserResponse(UserBase):
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True


# ---------------------- #
# ENDPOINTS              #
# ---------------------- #

from fastapi import Depends

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first()

#Can use by sending the following using postman post (new request -> http -> post (http://127.0.0.1:8000/users/) -> body -> raw -> JSON)
# {"detail":[{"type":"model_attributes_type","loc":["body"],"msg":"Input should be a valid dictionary or object to extract fields from","input":"{\r\n  \"full_name\": \"Sentient Shark\",\r\n  \"email\": \"shark@sentience.gov\",\r\n  \"user_role\": \"A Sentient Shark\"\r\n}"}]}

@app.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check unique email
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = User(
        full_name=user.full_name,
        email=user.email,
        user_role=user.user_role,
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

@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # If email is being updated, check uniqueness
    if user_update.email and user_update.email.lower() != user.email.lower():
        if get_user_by_email(db, user_update.email):
            raise HTTPException(status_code=400, detail="Email already registered")
    update_data = user_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return None

# ---------------------- #
# To run:
# uvicorn main:app --reload
# ---------------------- #

# Export Base for testing
Base = Base

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)