from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from file_system import *

app = FastAPI()
fs = FileSystem()


class CreateItem(BaseModel):
    path: str
    name: str
    is_directory: bool = False
    size: int = 0


class MoveItem(BaseModel):
    source_path: str
    dest_path: str


class SearchItem(BaseModel):
    name: str


@app.post("/create/")
def create_item(item: CreateItem):
    if fs.create(item.path, item.name, item.is_directory, item.size):
        return {"message": "Item created successfully"}
    else:
        raise HTTPException(status_code=400, detail="Invalid path or directory")


@app.delete("/delete/")
def delete_item(path: str):
    if fs.delete(path):
        return {"message": "Item deleted successfully"}
    else:
        raise HTTPException(status_code=400, detail="Invalid path")


@app.post("/move/")
def move_item(item: MoveItem):
    if fs.move(item.source_path, item.dest_path):
        return {"message": "Item moved successfully"}
    else:
        raise HTTPException(status_code=400, detail="Invalid source or destination path")


@app.get("/search/")
def search_item(name: str):
    result = fs.search(name)
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@app.get("/display/")
def display_tree():
    import io
    from contextlib import redirect_stdout
    f = io.StringIO()
    with redirect_stdout(f):
        fs.display_tree()
    return f.getvalue()


@app.get("/analyze/")
def analyze_item(path: str):
    result = fs.analyze(path)
    if result:
        total_size, file_count = result
        return {"total_size": total_size, "file_count": file_count}
    else:
        raise HTTPException(status_code=400, detail="Invalid path")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
