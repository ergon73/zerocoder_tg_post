import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import requests
import logging
from pathlib import Path

# --- Загрузка ключей из config.txt ---
def load_keys_from_config(config_path="config.txt"):
    keys = {}
    if Path(config_path).exists():
        with open(config_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    k, v = line.split('=', 1)
                    keys[k.strip()] = v.strip()
    return keys

config = load_keys_from_config()
openai_api_key = config.get("OPENAI_API_KEY")
currents_api_key = config.get("CURRENTS_API_KEY")

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("tgpost-debug")

logger.debug(f"[DEBUG] OPENAI_API_KEY: {openai_api_key}")
logger.debug(f"[DEBUG] CURRENTS_API_KEY: {currents_api_key}")

if not openai_api_key:
    logger.error("❌ Не задан OPENAI_API_KEY (в config.txt)")
    raise ValueError("❌ Не задан OPENAI_API_KEY (в config.txt)")
if not currents_api_key:
    logger.error("❌ Не задан CURRENTS_API_KEY (в config.txt)")
    raise ValueError("❌ Не задан CURRENTS_API_KEY (в config.txt)")

client = OpenAI(api_key=openai_api_key)

app = FastAPI()

class Topic(BaseModel):
    topic: str

def get_recent_news(topic: str) -> str:
    url = "https://api.currentsapi.services/v1/latest-news"
    params = {
        "language": "en",
        "keywords": topic,
        "apiKey": currents_api_key
    }
    logger.debug(f"[DEBUG] Currents API request params: {params}")
    response = requests.get(url, params=params)
    logger.debug(f"[DEBUG] Currents API response status: {response.status_code}")
    logger.debug(f"[DEBUG] Currents API response body: {response.text}")

    if response.status_code != 200:
        logger.error(f"Ошибка Currents API: {response.text}")
        raise HTTPException(status_code=500, detail=f"Ошибка Currents API: {response.text}")

    articles = response.json().get("news", [])
    if not articles:
        logger.info("Нет свежих новостей по теме")
        return "Нет свежих новостей"

    return "\n".join([f"- {article['title']}" for article in articles[:5]])

def generate_content(topic: str) -> dict:
    news_context = get_recent_news(topic)
    try:
        # Заголовок
        response_title = client.chat.completions.create(
            model="gpt-4o",
            messages=[{
                "role": "user",
                "content": f"Придумай привлекательный заголовок для статьи на тему '{topic}', с учетом новостей:\n{news_context}"
            }],
            max_tokens=60,
            temperature=0.5
        )
        if not response_title.choices or not hasattr(response_title.choices[0], "message"):
            logger.error(f"OpenAI не вернул заголовок: {response_title}")
            raise HTTPException(status_code=500, detail="OpenAI не вернул заголовок")
        title = response_title.choices[0].message.content.strip()

        # Мета-описание
        response_meta = client.chat.completions.create(
            model="gpt-4o",
            messages=[{
                "role": "user",
                "content": f"Напиши мета-описание для статьи с заголовком: '{title}'."
            }],
            max_tokens=100,
            temperature=0.5
        )
        if not response_meta.choices or not hasattr(response_meta.choices[0], "message"):
            logger.error(f"OpenAI не вернул мета-описание: {response_meta}")
            raise HTTPException(status_code=500, detail="OpenAI не вернул мета-описание")
        meta = response_meta.choices[0].message.content.strip()

        # Полный пост
        response_post = client.chat.completions.create(
            model="gpt-4o",
            messages=[{
                "role": "user",
                "content": (
                    f"Напиши подробную статью на тему '{topic}', опираясь на следующие новости:\n{news_context}\n"
                    "Статья должна быть структурированной, содержательной, с подзаголовками и выводами. Используй короткие абзацы."
                )
            }],
            max_tokens=1500,
            temperature=0.5
        )
        if not response_post.choices or not hasattr(response_post.choices[0], "message"):
            logger.error(f"OpenAI не вернул текст поста: {response_post}")
            raise HTTPException(status_code=500, detail="OpenAI не вернул текст поста")
        post = response_post.choices[0].message.content.strip()

        return {
            "title": title,
            "meta_description": meta,
            "post_content": post
        }

    except Exception as e:
        logger.error(f"Ошибка генерации контента: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка генерации контента: {str(e)}")

@app.post("/generate-post")
async def generate_post_api(payload: Topic):
    return generate_content(payload.topic)

@app.get("/")
def root():
    return {"message": "Service is running"}

@app.get("/heartbeat")
def heartbeat():
    return {"status": "OK"} 