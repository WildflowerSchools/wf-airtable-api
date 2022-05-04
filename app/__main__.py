import uvicorn

import app.main

if __name__ == "__main__":
    uvicorn.run(app.main.app)
