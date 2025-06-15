from fastapi import FastAPI
import redis, joblib, json, uvicorn
from ml.predict import top_users

app = FastAPI()
r = redis.Redis(host="redis", port=6379, decode_responses=True)
model = joblib.load("ml/propensity.pkl")

@app.get("/next/{user_id}")
def next_content(user_id: str):
    if cached := r.get(user_id):
        return json.loads(cached)
    recs = top_users(100)
    choice = recs.sample(1).iloc[0].to_dict()
    r.setex(user_id, 300, json.dumps(choice))
    return choice

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
