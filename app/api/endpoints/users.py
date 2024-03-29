from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.crud.users import users as users_crud
from app.db.database import getDB
from app.logger import create_logger
from app.schemas.users import (
    UserFollow,
    UserProfile,
    UserProfileModify,
    Users,
    UserTokenNotification,
    UserWithTransactionHash,
)

from .notifications import sendNotification
from .wallet import deposit, rechargeAWallet

logger = create_logger()

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

    # get user favourite to notify them
    userFavouriteObj = users_crud.get(db, Id=user_favourite)
    if not userFavouriteObj:
        raise HTTPException(
            status_code=404,
            detail="The user favourite does not exist in the system",
        )
    try:
        notifyUser = sendNotification(
            userFavouriteObj.tokenNotification,
            "You have a new follower",
            "You have a new follower",
            str(user_id),
            user.firstName,
        )
        if notifyUser['data']['status'] == 'error':
            raise HTTPException(
                status_code=404,
                detail="There were some error when notifiying the user favourite",
            )

    except HTTPException as e:
        raise HTTPException(
            status_code=409, detail="There was an error when notify the user favourite"
        ) from e

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
            logger.debug("The user %s does not exist in the system", userId)
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


# create PUT endpoint receiving user id and token notification
@router.put("/user_notification/{user_id}", response_model=UserTokenNotification)
def userNotification(
    *,
    db: Session = Depends(getDB),
    user_id: int,
    user_token_notification: str,
) -> Any:
    """
    Update a user with user notification.
    """
    user = users_crud.get(db, Id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user does not exist in the system",
        )

    userUpdated = users_crud.updateUserNotification(
        db, db_obj=user, tokenNotification=user_token_notification
    )
    return userUpdated


@router.put(
    "/newMessageNotification/{user_sender}/{user_addressee}", response_model=UserFollow
)
def newMessaNotification(
    *,
    db: Session = Depends(getDB),
    user_sender: int,
    user_addressee: int,
) -> UserProfile:
    """
    Send a notification to user_addressee.
    """

    userSender = users_crud.get(db, Id=user_sender)
    if not userSender:
        raise HTTPException(
            status_code=404,
            detail="The sender does not exist in the system",
        )

    userAddresseeObj = users_crud.get(db, Id=user_addressee)
    if not userAddresseeObj:
        raise HTTPException(
            status_code=404,
            detail="The addressee does not exist in the system",
        )

    try:
        notifyUser = sendNotification(
            userAddresseeObj.tokenNotification,
            "You have a new message",
            "You have a new message",
            str(userSender.id),
            userSender.firstName,
        )
        if notifyUser['data']['status'] == 'error':
            raise HTTPException(
                status_code=404,
                detail="There were some error when sending the notification",
            )

    except HTTPException as e:
        raise HTTPException(
            status_code=409, detail="There were an error when sending the notification"
        ) from e

    return userAddresseeObj


@router.get("/transactionHash/", response_model=List[UserWithTransactionHash])
def getTransactionHash(
    *,
    db: Session = Depends(getDB),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    '''
    Returns the transaction hash of the users.
    '''
    users = users_crud.get_multi(db, skip=skip, limit=limit)
    if not users:
        raise HTTPException(
            status_code=404,
            detail="There aren't any users.",
        )
    users_with_transaction_hash = []
    for user in users:
        logger.info("transaction hash: %s", {user.transactionHash})
        if user.transactionHash is not None:
            users_with_transaction_hash.append(
                UserWithTransactionHash(
                    id=int(user.id), transaction_hash=user.transactionHash
                )
            )
    return users_with_transaction_hash


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


@router.put("/premium_suscribe/{user_id}", response_model=UserProfile)
async def premiunSuscribe(
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
        transacionInformation = await deposit(user.privateKey, amount_to_deposit)
    except HTTPException as e:
        raise HTTPException(
            status_code=409, detail="There were an error making the deposit"
        ) from e

    userSuscribed = users_crud.suscribe(
        db, db_obj=user, transactionInfo=transacionInformation.json()
    )
    return userSuscribed


@router.put("/recharge_wallet/{user_id}", response_model=UserProfile)
def rechargeWallet(
    user_id: int,
    amount_to_deposit: float,
    db: Session = Depends(getDB),
) -> Any:
    """
    Recharge a wallet with ethers.
    """
    user = users_crud.get(db, Id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user does not exist in the system",
        )

    try:
        transacionInformation = rechargeAWallet(user.address, amount_to_deposit)
        logger.info("transactionInfor: %s", transacionInformation.json())
    except HTTPException as e:
        logger.error("error during a recharge a wallet: %s", e)
        raise HTTPException(
            status_code=409, detail="There were an error making the recharge"
        ) from e

    return user
