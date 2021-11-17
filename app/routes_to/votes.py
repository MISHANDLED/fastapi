from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import and_
from sqlalchemy.orm import Session
from .. import models, schemas
from ..oauth import get_curr_user
from ..database import get_db

router = APIRouter(
    prefix="/votes",
    tags=["VOTES"]
)


@router.post("/", status_code = status.HTTP_201_CREATED)
def vote(votes: schemas.Votes, db: Session = Depends(get_db), current_user: int = Depends(get_curr_user)):

    post_query = db.query(models.Post).filter(models.Post.id == votes.post_id).first()

    if not post_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {votes.post_id} not found")
    

    vote_query = db.query(models.Vote).filter(
        and_(
            models.Vote.post_id == votes.post_id, 
            models.Vote.user_id == current_user.id
        )
    )

    found_vote = vote_query.first()
    

    if(votes.dir ==1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail = f"User {current_user.username} has already voted")

        new_vote = models.Vote(user_id = current_user.id, post_id = votes.post_id)
        db.add(new_vote)
        db.commit()

        return{"Message":"Successful Voting"}

    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Vote does not exist")

        vote_query.delete(synchronize_session=False)
        db.commit()

        return{"Message":"Successful Un-Voting"}
    