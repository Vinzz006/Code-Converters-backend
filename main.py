import os
import sys
import pathlib

# Ensure root and backend are in sys.path
_root_dir = pathlib.Path(__file__).resolve().parent
_backend_dir = _root_dir / "backend"

if str(_root_dir) not in sys.path:
    sys.path.insert(0, str(_root_dir))
if str(_backend_dir) not in sys.path:
    sys.path.insert(0, str(_backend_dir))

from backend.main import app

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
