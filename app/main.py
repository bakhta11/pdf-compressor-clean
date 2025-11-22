#from fastapi import FastAPI
#from fastapi.middleware.cors import CORSMiddleware
#from app.api.routes import router as api_router


#def create_app() -> FastAPI:
#    app = FastAPI(
#        title="PDF + Word Compressor",
#        version="1.0.0"
#    )

    # CORS
#    app.add_middleware(
#        CORSMiddleware,
#        allow_origins=["*"],
#        allow_methods=["*"],
#        allow_headers=["*"],
#    )

    # Register all routes
#    app.include_router(api_router, prefix="/api")

#   return app


#app = create_app()



from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="PDF + Word Compressor",
        version="1.0.0",
        description="Upload PDF or Word files, convert to PDF, and compress with low/medium/high quality."
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register all API routes
    app.include_router(api_router, prefix="/api")

    return app


app = create_app()
