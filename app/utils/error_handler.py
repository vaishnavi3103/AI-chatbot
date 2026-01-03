from fastapi import HTTPException

def handle_exception(e):
    raise HTTPException(status_code=500, detail=str(e))