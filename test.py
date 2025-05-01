import httpx
import asyncio
from pprint import pprint
import random


async def get_jwt(student_id: str) -> str:
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "enumType": "student_id",
        "value": student_id
    }

    async with httpx.AsyncClient() as client:
        get_token_response = await client.post(
            'https://studev.kaowei.tw/api/token/get_token',
            headers=headers,
            data=data
        )
        token = random.choice(get_token_response.json()['token'])
        get_jwt_token_response = await client.post(
            'https://studev.kaowei.tw/api/token/request_jwt_token',
            headers=headers,
            data={
                "student_id": student_id,
                "token": token
            }
        )
        return get_jwt_token_response.json()['access_token']


async def main(student_id):
    token = ""
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "enumType": "student_id",
        "value": student_id
    }

    async with httpx.AsyncClient() as client:
        headers = {
            "Authorization": f"Bearer {get_jwt(student_id=student_id)}",
            "Accept": "application/json"
        }

        get_uuid_response = await client.get(f"https://studev.kaowei.tw/api/user?search_value={student_id}", headers=headers)

        user_uuid = get_uuid_response.json()['data'][0]['user_uuid']

        get_applicable_response = await client.get(f"https://studev.kaowei.tw/api/scholarship/apply/applicable?user_uuid={user_uuid}", headers=headers)

    pprint(get_applicable_response.json())
asyncio.run(main('000000'))
