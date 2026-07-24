import os
import httpx
from dotenv import load_dotenv

load_dotenv()

async def run_dify_workflow(question:str,user_id:str)-> str:
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                f"{os.environ['DIFY_API_BASE']}/workflow/run",
                headers={
                    "Authorization":f"Bearer {os.environ['DIFY_API_KEY']}",
                    "Content-Type":"application/json"
                },
                json={
                    "inputs":{"quesion":question},
                    "response_mode":"blocking",
                    "user":user_id
                }
            )
            response.raise_for_status()
    except httpx.HTTPError as exc:
        raise RuntimeError("Dify workflow request failed") from exc

    payload = response.json() # 这里是反序列化，将json转化为dict或者list，这里是dict
    data = payload.get("data",{}) # 这里表示从dict中取出data，如果没有就返回空dict

    if data.get("status") != "succeded":
        error = data.get("error") or "unknown workflow error"
        raise RuntimeError(f"Dify workflow failed: {error}")

    answer = data.get("outputs",{}).get("answer")
    if not isinstance(answer,str):
        raise RuntimeError("Dify workflow did not return string output: answer")
    return answer
