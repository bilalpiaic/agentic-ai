### **SQLAlchemy + Alembic + CRUD Operations**
This example covers:
1. **Foreign keys** in SQLAlchemy models
2. **CRUD operations** (Create, Read, Update, Delete)
3. **Alembic migration support**

---

## **1. Setup SQLAlchemy with Foreign Keys**
### **Install Dependencies**
```sh
pip install sqlalchemy alembic psycopg2-binary
```

---

### **2. Define Models with Foreign Keys**
```python
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

Base = declarative_base()

# User Model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    
    # Relationship with Post
    posts = relationship("Post", back_populates="user", cascade="all, delete")

# Post Model
class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    
    user = relationship("User", back_populates="posts")

# Database Connection
DATABASE_URL = "postgresql://user:password@localhost/mydatabase"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(engine)  # Create tables if they don't exist
```

---

## **3. Generate Alembic Migration**
```sh
alembic revision --autogenerate -m "Add users and posts table"
alembic upgrade head
```

---

## **4. CRUD Operations for User and Post**

```python
from sqlalchemy.orm import Session

# Create User
def create_user(db: Session, name: str):
    user = User(name=name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Read User by ID
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# Read All Users
def get_users(db: Session):
    return db.query(User).all()

# Update User
def update_user(db: Session, user_id: int, new_name: str):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.name = new_name
        db.commit()
        db.refresh(user)
    return user

# Delete User (Cascade Deletes Posts)
def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user

# Create Post
def create_post(db: Session, title: str, user_id: int):
    post = Post(title=title, user_id=user_id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

# Read Posts by User ID
def get_posts_by_user(db: Session, user_id: int):
    return db.query(Post).filter(Post.user_id == user_id).all()

# Update Post
def update_post(db: Session, post_id: int, new_title: str):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        post.title = new_title
        db.commit()
        db.refresh(post)
    return post

# Delete Post
def delete_post(db: Session, post_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        db.delete(post)
        db.commit()
    return post
```

---

## **5. Running the CRUD Operations**
```python
db = SessionLocal()

# Create a new user
user = create_user(db, "John Doe")
print("User Created:", user)

# Create a post for the user
post = create_post(db, "My First Post", user.id)
print("Post Created:", post)

# Read all users
users = get_users(db)
print("All Users:", users)

# Update user
updated_user = update_user(db, user.id, "John Updated")
print("Updated User:", updated_user)

# Delete user (deletes posts too)
delete_user(db, user.id)
print("User Deleted")
```

---

## **Conclusion**
- **Foreign keys** ensure data integrity.
- **Alembic** handles migrations.
- **CRUD functions** allow seamless data management.