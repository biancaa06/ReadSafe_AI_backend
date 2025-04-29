from fastapi.middleware.cors import CORSMiddleware

def configure_cors(app):
    origins = [
        "http://localhost:5173",
        "https://read-safe-ai-frontend-oimz.vercel.app/"
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
