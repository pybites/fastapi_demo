from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()


class Bite(BaseModel):
    name: Optional[str]
    description: Optional[str] = None
    level: int = 1
    tags: List[str] = []


bites = {
    1: {"name": "Sum of numbers", "level": 2},
    2: {"name": "Regex fun", "description": "regex are ...", "level": 4},
    3: {"name": "Word values", "level": 3},
}


@app.get("/", status_code=200)
async def get_bites():
    return bites


@app.get("/{bite_id}", status_code=200)
async def get_bite(bite_id: int):
    bite = bites.get(bite_id)
    if bite is None:
        raise HTTPException(status_code=404, detail="Bite not found")
    return bite


@app.post("/", status_code=201)
async def create_bite(bite: Bite):
    new_bite_id = max(bites) + 1
    bites[new_bite_id] = bite
    return bite


@app.put("/{bite_id}", status_code=200)
async def update_bite(bite_id: int, bite: Bite):
    if bite_id not in bites:
        raise HTTPException(status_code=404, detail="Bite not found")
    bites[bite_id] = bite
    return bite


@app.delete("/{bite_id}", status_code=204)
async def delete_bite(bite_id: int):
    try:
        del bites[bite_id]
        return {}
    except KeyError:
        raise HTTPException(status_code=404, detail="Bite not found")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
