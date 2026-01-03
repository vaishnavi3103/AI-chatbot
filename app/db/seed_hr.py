import json
from app.db.mongo import hr_collection


def seed_hr():
    # Already loaded? Then skip.
    if hr_collection.estimated_document_count() > 0:
        return

    with open("app/data/hr.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    hr_collection.insert_many(data)
