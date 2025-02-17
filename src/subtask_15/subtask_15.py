from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from subtask_06.subtask_06 import parse_all_pathways, build_drug_pathway_counts
import os

app = FastAPI()

class DrugRequest(BaseModel):
    drug: str

@app.post("/drug_count")
async def get_drug_count(request: DrugRequest):
    # XML file path
    file_path = os.path.join(os.path.dirname(__file__), "..", "drugbank_partial.xml")
    try:
        pathways = parse_all_pathways(file_path)
        drug_counts = build_drug_pathway_counts(pathways)
        count = drug_counts.get(request.drug)
        if count is None:
            raise HTTPException(status_code=404, detail="Drug not found")
        return {"drug": request.drug, "pathway_count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
