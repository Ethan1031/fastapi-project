from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from typing import Optional, List

router = APIRouter(
    prefix='/vote',
    tags = ['Vote']
)

@router.post("/", status_code = status.HTTP_201_CREATED)
# 1. validate data types in schemas class vote. 
# 2. Link to database
# 3. Ensure it login with authentication and return current_user
def vote(vote: schemas.vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # Checking to ensure that post id you vote is existing in table.
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {vote.post_id} does not exist")
    # Check if the vote is already existing
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail = f"user {current_user.id} has already vote on post {vote.post_id}")
        # If not found it, then add the vote
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post {vote.post_id} does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted vote"}
