from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from typing import Optional, List
from sqlalchemy import func

router = APIRouter(
    prefix='/posts',
    tags = ['Post']
)

# Using SQL example: 
# @app.get("/posts")
# def get_posts():
#     cursor.execute(""" Select * from posts """)
#     posts = cursor.fetchall()
#     return {"data": posts}

# @app.post("/posts", status_code = status.HTTP_201_CREATED)
# def create_posts(post: Post):
#     cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) returning * """, 
#     (post.title, post.content, post.published))
#     new_post = cursor.fetchone()
#     conn.commit()
#     return {"data": new_post}

# @app.get("/posts/{id}")
# def get_posts(id: int):
#     cursor.execute("""SELECT * FROM posts where id = %s """, (str(id)))
#     post = cursor.fetchone()
#     if not post: 
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail = f"post with id: {id} was not found")
#     return {"post_details": post}

# @app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
#     deleted_post = cursor.fetchone()
#     conn.commit()

#     if deleted_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail = f"post with id: {id} was not found")
#     return Response(status_code = status.HTTP_204_NO_CONTENT)

# @app.put("/posts/{id}")
# def update_post(id: int, post: Post):
#     published = post.published if hasattr(post, "published") and post.published is not None else False
#     cursor.execute(
#             """UPDATE posts 
#             SET title = %s, content = %s, published = %s 
#             WHERE id = %s 
#             RETURNING *""",
#             (post.title, post.content, published, str(id))
#         )
#     updated_post = cursor.fetchone()
#     conn.commit()

#     # Handle case when the post is not found
#     if updated_post is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Post with id: {id} was not found"
#         )
#     return {"data": updated_post}

# Using python to call model function within fastapi: 
# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"data": posts}

# Instaed of using dictonary form as return data, we just directly return post
# Python will automatically convert it into json format
# return {"data": post_query.first()}
# return post_query.first()

# Get all posts
# When responding, we need a list of post, to get all posts
@router.get("/", response_model = List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
              Limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()

    result = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(
        models.Post.id).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()
    return result

# put db: Session = Depends(get_db) as a path operation function to ensure 
# we give us a access to database object that we can actually make queies and make changes to database.
@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # to make it more sufficient, we not need to write it again and again
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Getting an individual post
@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # Code before 
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    # We want to get the vote number as well when we view the post
    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(
        models.Post.id)
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id: {id} was not found")
    return post

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} was not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail = f"Not authorized to delete this post")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    # Handle case when the post is not found
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail = f"Not authorized to delete this post")
    post_query.update(updated_post.dict(), synchronize_session = False)
    db.commit()
    return post_query.first()

