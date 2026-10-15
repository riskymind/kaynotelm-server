from fastapi import APIRouter, HTTPException


router = APIRouter(tags=["Health Routes"])

# Health check endpoints
@router.get("/")
async def root():
    return {"message": "KayNoteLM AI Engineering app is running!"}


@router.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}