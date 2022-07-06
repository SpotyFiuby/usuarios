from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.crud.crud_users import users as users_crud
from app.db.database import getDB
from app.schemas.users import UserFollow, UserProfile, UserProfileModify, Users

from .wallet import deposit

router = APIRouter()


@router.get("/", response_model=List[UserProfile])
def readUsers(
    db: Session = Depends(getDB),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve users.
    """
    users = users_crud.get_multi(db, skip=skip, limit=limit)
    if not users:
        raise HTTPException(
            status_code=404,
            detail="There aren't any users.",
        )
    return users


@router.get("/{user_id}", response_model=UserProfile)
def readUserByID(
    user_id: int,
    db: Session = Depends(getDB),
) -> Any:
    """
    Get a specific user by id.
    """
    user = users_crud.get(db, Id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user does not exist in the system",
        )
    return user


@router.put("/{user_id}", response_model=UserProfileModify)
def updateUser(
    *,
    db: Session = Depends(getDB),
    user_id: int,
    user_in: UserProfileModify,
) -> Any:
    """
    Update a user.
    """
    user = users_crud.get(db, Id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user does not exist in the system",
        )
    user = users_crud.update(db, db_obj=user, obj_in=user_in)
    return user


@router.delete("/{user_id}", response_model=Users)
def deleteUser(
    *,
    db: Session = Depends(getDB),
    user_id: int,
) -> Any:
    """
    Delete an user.
    """
    user = users_crud.get(db, Id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user = users_crud.remove(db=db, Id=user_id)
    return user


@router.get("/email/{user_email}", response_model=UserProfile)
def readUserByEmail(
    user_email: EmailStr,
    db: Session = Depends(getDB),
) -> Any:
    """
    Get a specific user by email.
    """
    user = users_crud.get_by_email(db, email=user_email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user does not exist in the system",
        )
    return user


@router.get("/search_prefix_email/{user_email}", response_model=List[UserProfile])
def searchPrefixUsers(
    email_prefix: str, limit: int = 100, db: Session = Depends(getDB)
) -> Any:
    """
    Retrieve users by a certain criteria.
    """
    users = users_crud.user_email_prefix(db, emailPrefix=email_prefix, limit=limit)
    if not users:
        raise HTTPException(
            status_code=404,
            detail="There aren't any users with the search criteria.",
        )
    return users


@router.put("/user_artist_followers/{user_id}", response_model=UserFollow)
def userArtistFollowers(
    *,
    db: Session = Depends(getDB),
    user_id: int,
    user_favourite: int,
) -> Any:
    """
    Update a user with user followers.
    """
    user = users_crud.get(db, Id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user does not exist in the system",
        )

    userUpdated = users_crud.updateUserFollowers(
        db, db_obj=user, obj_follower=user_favourite
    )
    return userUpdated


@router.put("/user_artist_followings/{user_id}", response_model=UserFollow)
def userArtistFollowings(
    *,
    db: Session = Depends(getDB),
    user_id: int,
    user_favourite: int,
) -> Any:
    """
    Update a user with user following.
    """
    user = users_crud.get(db, Id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user does not exist in the system",
        )

    userUpdated = users_crud.updateUserFollowing(
        db, db_obj=user, obj_following=user_favourite
    )
    return userUpdated


@router.delete(
    "/user_artist_followings/{user_id}/{artist_id}", response_model=UserFollow
)
def deleteUserArtistFollowings(
    *,
    db: Session = Depends(getDB),
    user_id: int,
    user_favourite: int,
) -> Any:
    """
    Delete a user from a followings list.
    """
    user = users_crud.get(db, Id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user does not exist in the system",
        )

    userUpdated = users_crud.deleteUserFromFollowing(
        db, db_obj=user, obj_following=user_favourite
    )
    return userUpdated


@router.delete("/user_artist_follower/{user_id}/{artist_id}", response_model=UserFollow)
def deleteUserArtistFollowers(
    *,
    db: Session = Depends(getDB),
    user_id: int,
    user_favourite: int,
) -> Any:
    """
    Delete a user from a followers list.
    """
    user = users_crud.get(db, Id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user does not exist in the system",
        )

    userUpdated = users_crud.deleteUserFromFollower(
        db, db_obj=user, obj_follower=user_favourite
    )
    return userUpdated


@router.get("/followers_amount/")
def getFollowersAmount(
    *,
    db: Session = Depends(getDB),
    user_id: int,
) -> Any:
    """
    Retrieve user followers.
    """
    user = users_crud.get(db, Id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user does not exist in the system",
        )
    followers_amount = users_crud.get_amounts_of_followers(db_obj=user)
    return followers_amount


@router.get("/followings_amount/")
def getFollowingsAmount(
    *,
    db: Session = Depends(getDB),
    user_id: int,
) -> Any:
    """
    Retrieve user followings.
    """
    user = users_crud.get(db, Id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user does not exist in the system",
        )
    followers_amount = users_crud.get_amounts_of_followings(db_obj=user)
    return followers_amount


def getFollowUser(db, idsList):
    followers = []
    for userId in idsList:
        user = users_crud.get(db, Id=userId)
        if not user:
            print("user id: {} not found".format(id))
        followers.append(user)

    return followers


@router.get("/user_followers/{user_id}", response_model=List[UserProfile])
def getFollowersProfile(
    user_id: int,
    db: Session = Depends(getDB),
) -> Any:
    """
    Retrieve user followers profile.
    """
    user = users_crud.get(db, Id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user does not exist in the system",
        )
    followersList = user.followers
    return getFollowUser(db, followersList)


@router.get("/user_followings/{user_id}", response_model=List[UserProfile])
def getFollowingsProfile(
    user_id: int,
    db: Session = Depends(getDB),
) -> Any:
    """
    Retrieve user followings profile.
    """
    user = users_crud.get(db, Id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user does not exist in the system",
        )
    followingsList = user.following
    return getFollowUser(db, followingsList)


@router.put("/user_unsuscribe/{user_id}", response_model=UserProfile)
def unsuscribeContent(
    user_id: int,
    db: Session = Depends(getDB),
) -> Any:
    """
    Unsuscribe to content.
    """
    user = users_crud.get(db, Id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user does not exist in the system",
        )
    userUnsuscribed = users_crud.unsuscribe(db, db_obj=user)
    return userUnsuscribed


@router.put("/user_suscribe/{user_id}", response_model=UserProfile)
def suscribeContent(
    user_id: int,
    amount_to_deposit: float,
    db: Session = Depends(getDB),
) -> Any:
    """
    Suscribe to content.
    """
    user = users_crud.get(db, Id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user does not exist in the system",
        )

    try:
        transacionInformation = deposit(user.id, amount_to_deposit)
    except HTTPException as e:
        raise HTTPException(
            status_code=409, detail="There were an error making the deposit"
        ) from e

    userSuscribed = users_crud.suscribe(
        db, db_obj=user, transactionInfo=transacionInformation.json()
    )
    return userSuscribed
