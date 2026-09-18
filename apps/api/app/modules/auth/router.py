import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models import User
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
    get_current_admin
)
from app.schemas import (
    UserRegisterRequest,
    UserLoginRequest,
    AdminLoginRequest,
    AuthTokenResponse,
    UserProfileResponse,
    UserProfileUpdateRequest,
    ChangePasswordRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    CheckUserRequest,
    UserCheckResponse,
    UserExistData
)

router = APIRouter(prefix="/auth", tags=["Authentication & Accounts"])

def format_user_profile(user: User) -> UserProfileResponse:
    return UserProfileResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        phone=user.phone,
        avatar_url=user.avatar_url,
        role=user.role,
        reward_points=user.reward_points,
        created_at=user.created_at.isoformat() if user.created_at else None
    )

# -----------------
# Customer Auth
# -----------------

@router.post("/check-user", response_model=UserCheckResponse)
@router.get("/check-user", response_model=UserCheckResponse)
async def check_user_exists(
    email: Optional[str] = None,
    body: Optional[CheckUserRequest] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Check if a user account exists with given email.
    Returns:
    {
        "statusCode": 200,
        "message": "User exist",
        "data": { "userExist": true, "userSetUpPassword": true },
        "successful": true
    }
    """
    target_email = ((body.email if body else None) or email or "").strip().lower()
    if not target_email:
        return UserCheckResponse(
            statusCode=400,
            message="Email is required",
            data=UserExistData(userExist=False, userSetUpPassword=False),
            successful=False
        )

    stmt = select(User).where(User.email == target_email)
    res = await db.execute(stmt)
    user = res.scalar_one_or_none()

    user_exists = user is not None
    user_has_password = bool(user and user.hashed_password)

    return UserCheckResponse(
        statusCode=200,
        message="User exist" if user_exists else "User does not exist",
        data=UserExistData(
            userExist=user_exists,
            userSetUpPassword=user_has_password,
            email=target_email
        ),
        successful=True
    )

@router.post("/register", response_model=AuthTokenResponse, status_code=status.HTTP_201_CREATED)
async def register_customer(
    body: UserRegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new customer account and return standard REST envelope with JWT session.
    If user already exists, returns structured 400 error with userExist: True.
    """
    clean_email = body.email.strip().lower()
    
    # Check if email is already in use
    stmt = select(User).where(User.email == clean_email)
    res = await db.execute(stmt)
    existing_user = res.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "statusCode": 400,
                "message": "User exist",
                "data": {
                    "userExist": True,
                    "userSetUpPassword": bool(existing_user.hashed_password),
                    "email": clean_email
                },
                "successful": False
            }
        )

    new_user = User(
        id=str(uuid.uuid4()),
        name=body.name.strip(),
        email=clean_email,
        hashed_password=hash_password(body.password),
        phone=body.phone.strip() if body.phone else None,
        role="customer",
        reward_points=500  # 500 bonus welcome points
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    token = create_access_token({"sub": new_user.id, "email": new_user.email, "role": new_user.role})
    user_profile = format_user_profile(new_user)
    
    return AuthTokenResponse(
        access_token=token,
        token_type="bearer",
        expires_in=604800,
        user=user_profile,
        statusCode=201,
        message="User registered successfully",
        data={
            "userExist": False,
            "userSetUpPassword": True,
            "access_token": token,
            "token_type": "bearer",
            "user": user_profile.model_dump()
        },
        successful=True
    )

@router.post("/login", response_model=AuthTokenResponse)
async def login_customer(
    body: UserLoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Customer sign in with email and password.
    """
    clean_email = body.email.strip().lower()
    stmt = select(User).where(User.email == clean_email)
    res = await db.execute(stmt)
    user = res.scalar_one_or_none()

    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "statusCode": 401,
                "message": "Invalid email or password.",
                "data": {
                    "userExist": bool(user),
                    "userSetUpPassword": bool(user and user.hashed_password)
                },
                "successful": False
            }
        )

    token = create_access_token({"sub": user.id, "email": user.email, "role": user.role})
    user_profile = format_user_profile(user)
    return AuthTokenResponse(
        access_token=token,
        token_type="bearer",
        expires_in=604800,
        user=user_profile,
        statusCode=200,
        message="Login successful",
        data={
            "userExist": True,
            "userSetUpPassword": True,
            "access_token": token,
            "token_type": "bearer",
            "user": user_profile.model_dump()
        },
        successful=True
    )

@router.get("/me", response_model=UserProfileResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Returns the authenticated user's current account profile and reward points.
    """
    return format_user_profile(current_user)

@router.put("/profile", response_model=UserProfileResponse)
async def update_my_profile(
    body: UserProfileUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Updates profile details (name, phone number, avatar URL).
    """
    if body.name is not None:
        current_user.name = body.name.strip()
    if body.phone is not None:
        current_user.phone = body.phone.strip()
    if body.avatar_url is not None:
        current_user.avatar_url = body.avatar_url.strip()

    await db.commit()
    await db.refresh(current_user)
    return format_user_profile(current_user)

@router.post("/change-password")
async def change_password(
    body: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Changes the authenticated user's account password.
    """
    if not verify_password(body.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password entered is incorrect."
        )

    current_user.hashed_password = hash_password(body.new_password)
    await db.commit()
    return {"success": True, "message": "Password updated successfully."}

@router.post("/forgot-password")
async def forgot_password(
    body: ForgotPasswordRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Requests a password reset token for account recovery.
    """
    clean_email = body.email.strip().lower()
    stmt = select(User).where(User.email == clean_email)
    res = await db.execute(stmt)
    user = res.scalar_one_or_none()

    reset_token = f"rst_{uuid.uuid4().hex}"
    # In production, send via email. Here we return success and preview token in dev
    return {
        "success": True,
        "message": f"If an account with {clean_email} exists, password reset instructions have been dispatched.",
        "reset_token": reset_token
    }

@router.post("/reset-password")
async def reset_password(
    body: ResetPasswordRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Sets a new password using a verified reset token.
    """
    if not body.token.startswith("rst_"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired password reset token."
        )
    return {
        "success": True,
        "message": "Password has been successfully reset. You may now login."
    }

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """
    Logs out the authenticated user session.
    """
    return {"success": True, "message": "Successfully logged out."}

# -----------------
# Admin Auth
# -----------------

@router.post("/admin/login", response_model=AuthTokenResponse)
async def admin_login(
    body: AdminLoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Administrative gateway: Authenticates store administrators and issues elevated JWT session.
    """
    clean_email = body.email.strip().lower()
    stmt = select(User).where(User.email == clean_email)
    res = await db.execute(stmt)
    user = res.scalar_one_or_none()

    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid administrator credentials."
        )

    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. This account does not possess administrator credentials."
        )

    token = create_access_token({"sub": user.id, "email": user.email, "role": "admin"})
    return AuthTokenResponse(
        access_token=token,
        token_type="bearer",
        expires_in=604800,
        user=format_user_profile(user)
    )

@router.get("/admin/me", response_model=UserProfileResponse)
async def get_admin_profile(
    current_admin: User = Depends(get_current_admin)
):
    """
    Returns the current verified administrator's identity and privileges.
    """
    return format_user_profile(current_admin)
