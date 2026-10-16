from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.userRoutes import router as userRoutes
from routes.healthRoutes import router as HealthRoutes
from routes.projectRoutes import router as ProjectRoutes
from routes.projectFilesRoutes import router as ProjectFilesRoutes
from routes.chatRoutes import router as ChatRoutes

# Create FastAPI app
app = FastAPI(
    title="Kaynotelm AI Engineering API",
    description="Backend API for KayNoteLM AI Engineering application",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(userRoutes, prefix="/api/user")
app.include_router(HealthRoutes, prefix="/api/health")
app.include_router(ProjectRoutes, prefix="/api/projects")
app.include_router(ProjectFilesRoutes, prefix="/api/projects")
app.include_router(ChatRoutes, prefix="/api/chats")

