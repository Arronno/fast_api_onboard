import os
import uuid
import shutil
import tempfile

from sqlalchemy import select
from app.images import imagekit
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import PostCreate, PostResponse, UserRead, UserCreate, UserUpdate
from app.database import User, Post, create_db_and_tables, get_async_session
from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from app.users import auth_backend, current_active_user, fastapi_users


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


fast_app = FastAPI(lifespan=lifespan)

fast_app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
fast_app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
fast_app.include_router(
    fastapi_users.get_reset_password_router(), prefix="/auth", tags=["auth"]
)
fast_app.include_router(
    fastapi_users.get_verify_router(UserRead), prefix="/auth", tags=["auth"]
)
fast_app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate), prefix="/auth", tags=["auth"]
)


@fast_app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    caption: str = Form(""),
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    temp_file_path = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=os.path.splitext(file.filename)[1]
        ) as temp_file:
            # temp file only holds the content of the file with provided ext
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)

        upload_result = imagekit.files.upload(
            file=open(temp_file_path, "rb"),
            file_name=file.filename,  # gets proper filename
            use_unique_file_name=True,
            tags=["backend-upload"],
        )

        post = Post(
            user_id=user.id,
            caption=caption,
            url=upload_result.url,
            file_type="video" if file.content_type.startswith("video/") else "image",
            file_name=upload_result.name,
        )

        session.add(post)
        await session.commit()
        await session.refresh(post)

        return post

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        file.file.close()


@fast_app.get("/feed")
async def get_feed(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]

    result = await session.execute(select(User))
    users = [row[0] for row in result.all()]
    user_dict = {user.id: user.email for user in users}

    posts_data = []
    for post in posts:
        posts_data.append(
            {
                "post_id": str(post.post_id),
                "user_id": str(post.user_id),
                "caption": post.caption,
                "url": post.url,
                "file_type": post.file_type,
                "file_name": post.file_name,
                "created_at": post.created_at.isoformat(),
                "is_owner": post.user_id == user.id,
                "email": user_dict.get(post.user_id, "Unknown"),
            }
        )

    return {"posts": posts_data}


@fast_app.delete("/posts/{post_id}")
async def delete_post(
    post_id: str,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    try:
        post_uuid = uuid.UUID(post_id)

        result = await session.execute(select(Post).where(Post.post_id == post_uuid))
        post = result.scalars().first()

        if not post:
            raise HTTPException(status_code=404, detail="Post Not Found")

        if post.user_id != user.id:
            raise HTTPException(status_code=403, detail="Permission Denied!")

        await session.delete(post)
        await session.commit()

        return {"success": True, "message": f"Post [{post_id}] Deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
