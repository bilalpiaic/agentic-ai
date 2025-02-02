from fastapi import APIRouter

authRouter = APIRouter()

@authRouter.post("/register")
async def register():
    return {"message": "Register"}

@authRouter.post("/login")
async def login():
    return {"message": "Login"}

@authRouter.post("/logout")
async def logout():
    return {"message": "Logout"}

@authRouter.post("/forgot-password")
async def forgot_password():
    return {"message": "Forgot password"}