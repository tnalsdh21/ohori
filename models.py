from bson.objectid import ObjectId
from datetime import datetime

# USER 컬렉션 CRUD
async def create_user(db, user_data):
    result = await db["users"].insert_one(user_data)
    return str(result.inserted_id)

async def get_user(db, user_id):
    user = await db["users"].find_one({"_id": ObjectId(user_id)})
    if user:
        user["_id"] = str(user["_id"])
    return user

async def update_user(db, user_id, update_data):
    result = await db["users"].update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
    return result.modified_count > 0

async def delete_user(db, user_id):
    result = await db["users"].delete_one({"_id": ObjectId(user_id)})
    return result.deleted_count > 0

# GPT_RESPONSE 컬렉션
async def insert_gpt_response(db, story_id, choices, metadata):
    result = await db["gpt_responses"].insert_one({
        "story_id": story_id,
        "choices": choices,
        "metadata": metadata
    })
    return str(result.inserted_id)


# ANSWER 컬렉션
async def insert_answer(db, user_id, story_id, choice):
    result = await db["answers"].insert_one({
        "user_id": user_id,
        "story_id": story_id,
        "choice": choice,
        "created_at": datetime.now()
    })
    return str(result.inserted_id)
