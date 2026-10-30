from fastapi import FastAPI, HTTPException
from app.schemas import PostCreate, PostResponse

fast_app = FastAPI()


text_posts = {
    1: {"name": "t1", "content": "cool product"},
    2: {"name": "t2", "content": "smart device"},
    3: {"name": "t3", "content": "wireless headphones"},
    4: {"name": "t4", "content": "gaming laptop"},
    5: {"name": "t5", "content": "portable charger"},
    6: {"name": "t6", "content": "mechanical keyboard"},
    7: {"name": "t7", "content": "fitness tracker"},
    8: {"name": "t8", "content": "bluetooth speaker"},
    9: {"name": "t9", "content": "smartwatch"},
    10: {"name": "t10", "content": "4K monitor"},
}


@fast_app.get("/")
def landing_page():
    return {"message": "Landing Page!"}


@fast_app.get("/home")
def home():
    return {"message": "Welcome!"}


@fast_app.get("/posts/{post_id}")
def get_post(post_id: int) -> PostResponse:
    if post_id not in text_posts:
        raise HTTPException(status_code=404, detail="Post Not Found")
    return text_posts.get(post_id)


@fast_app.get("/posts")
def get_all_posts(limit: int = None):
    if limit is not None:
        return list(text_posts.values())[:limit]
    else:
        return list(text_posts.values())


@fast_app.post("/posts")
def create_post(post: PostCreate) -> PostResponse:
    new_post = {"name": post.name, "content": post.content}
    text_posts[max(text_posts.keys()) + 1] = new_post
    return new_post
