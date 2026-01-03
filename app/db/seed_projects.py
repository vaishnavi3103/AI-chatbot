import json
from app.db.mongo import project_collection


def seed_projects():
    if project_collection.estimated_document_count() > 0:
        return

    with open("app/data/project.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    project_collection.insert_many(data)
