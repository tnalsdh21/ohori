from fastapi import HTTPException
from fastapi import FastAPI
from pydantic import BaseModel
from gpt import generate_response
from database import connect_to_mongo, close_mongo_connection, mongo
from models import create_user, get_user, update_user, delete_user, insert_gpt_response, insert_answer
app = FastAPI()

# 요청 바디 모델 정의
class PromptRequest(BaseModel):
    prompt: str

# 데이터 모델 정의
class User(BaseModel):
    username: str
    email: str
    gender: str
    position: str #현재 레벨 , 최종목표

class GPTResponse(BaseModel):
    story_id: str #레벨에 맞는 시나리오 주제들의 고유번호 
    choices: list  #-> 각 시나리오마다 응답한 선택지들(별도컬렉션이 필요하면 중첩 컬렉션도 가능) 
    metadata: dict

class Answer(BaseModel): #사용자가 선택한 응답
    user_id: str
    story_id: str
    choice: str

# MongoDB 연결 설정
@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

# OPENAI API 
# prompt 가 여러개일텐데 그에 따라 gpt_reponse 에 insert 하는 함수 만들건지 
# 아래 generate 모듈로 호출한건지 선택 가능
@app.post("/generate")
async def generate(prompt_request: PromptRequest):
    prompt = prompt_request.prompt
    response = generate_response(prompt)
    return {"response": response}

# USER CRUD API
@app.post("/users/")
async def create_user_endpoint(user: User):
    user_id = await create_user(mongo.db, user.dict())
    return {"user_id": user_id}

@app.get("/users/{user_id}")
async def get_user_endpoint(user_id: str):
    user = await get_user(mongo.db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}")
async def update_user_endpoint(user_id: str, user: User):
    success = await update_user(mongo.db, user_id, user.dict())
    if not success:
        raise HTTPException(status_code=404, detail="User not found or no changes made")
    return {"message": "User updated"}

@app.delete("/users/{user_id}")
async def delete_user_endpoint(user_id: str):
    success = await delete_user(mongo.db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}

# GPT_RESPONSE API
@app.post("/gpt_responses/")
async def create_gpt_response(gpt_response: GPTResponse):
    response_id = await insert_gpt_response(
        mongo.db,
        gpt_response.story_id,
        gpt_response.choices,
        gpt_response.metadata
    )
    return {"response_id": response_id}

# ANSWER API
@app.post("/answers/")
async def create_answer(answer: Answer):
    answer_id = await insert_answer(
        mongo.db,
        answer.user_id,
        answer.story_id,
        answer.choice
    )
    return {"answer_id": answer_id}