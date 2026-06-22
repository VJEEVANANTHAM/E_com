# # # import psycopg2

# # # DATABASE_URL = "postgresql://postgres:1235@localhost:5433/multillm_gateway"

# # # try:
# # #     conn = psycopg2.connect(DATABASE_URL)
# # #     cursor = conn.cursor()
# # #     cursor.execute("SELECT 1;")

# # #     print("PostgreSQL URL is working ✅")
# # #     print(cursor.fetchone())

# # #     cursor.close()
# # #     conn.close()

# # # except Exception as e:
# # #     print("PostgreSQL URL not working ❌")
# # #     print(e)

# # # import time

# # # def task():
# # #     print("Start")
# # #     time.sleep(3)
# # #     print("End")

# # # task()


# # # async def download_file(name):
# # #     print(f"Start downloading {name}")
# # #     await asyncio.sleep(3)
# # #     print(f"Finished downloading {name}")

# # # async def main():
# # #     await asyncio.gather(
# # #         download_file("file1"),
# # #         download_file("file2"),
# # #         download_file("file3"),
# # #     )

# # # import asyncio

# # # async def task(name):
# # #     print("start", name)
# # #     await asyncio.sleep(3)
# # #     print("end", name)

# # # async def main():
# # #     await asyncio.gather(
# # #         task("A"),
# # #         task("B"),
# # #         task("C")
# # #     )

# # # asyncio.run(main())
# # # asyncio.run(main())

# # from fastapi import FastAPI, HTTPException
# # import requests
# # import httpx
# # import time
# # import asyncio

# # app = FastAPI()


# # # # -----------------------------
# # # # 1. Normal sync API
# # # # -----------------------------
# # # @app.get("/sync-users")
# # # def get_users_sync():
# # #     start_time = time.time()

# # #     try:
# # #         response = requests.get("https://dummyjson.com/users", timeout=10)
# # #         response.raise_for_status()

# # #         end_time = time.time()

# # #         return {
# # #             "type": "sync",
# # #             "time_taken": round(end_time - start_time, 2),
# # #             "data": response.json()
# # #         }

# # #     except requests.exceptions.Timeout:
# # #         raise HTTPException(status_code=504, detail="Dummy API timeout")

# # #     except requests.exceptions.RequestException as e:
# # #         raise HTTPException(status_code=500, detail=str(e))


# # # # -----------------------------
# # # # 2. Async API
# # # # -----------------------------
# # # @app.get("/async-users")
# # # async def get_users_async():
# # #     start_time = time.time()

# # #     try:
# # #         async with httpx.AsyncClient() as client:
# # #             response = await client.get("https://dummyjson.com/users", timeout=10)

# # #         response.raise_for_status()

# # #         end_time = time.time()

# # #         return {
# # #             "type": "async",
# # #             "time_taken": round(end_time - start_time, 2),
# # #             "data": response.json()
# # #         }

# # #     except httpx.TimeoutException:
# # #         raise HTTPException(status_code=504, detail="Dummy API timeout")

# # #     except httpx.HTTPError as e:
# # #         raise HTTPException(status_code=500, detail=str(e))
# # @app.get("/payment")
# # async def payment():
# #     await asyncio.sleep(100)
# #     return {"message": "payment completed"}

# # # @app.get("/payment1")
# # # def payment1():
# # #     # await asyncio.sleep(100)
# # #     time.sleep(100)
# # #     return {"message": "payment completed"}


# # @app.get("/profile")
# # async def profile():
# #     return {"message": "profile loaded"}

# from fastapi import FastAPI
# import asyncio,time
# app=FastAPI()

# @app.get("/payment")
# def payment():
#     # await asyncio.sleep(100)
#     time.sleep(100)
#     return {"message": "payment completed"}

# # @app.get("/payment1")
# # def payment1():
# #     # await asyncio.sleep(100)
# #     time.sleep(100)
# #     return {"message": "payment completed"}


# @app.get("/profile")
# def profile():
#     return {"message": "profile loaded"}

from fastapi import FastAPI
import time
import threading
import anyio.to_thread

app = FastAPI()


@app.get("/payment")
def payment():
    # print("PAYMENT started:", threading.current_thread().name)
    time.sleep(30)
    # print("PAYMENT finished:", threading.current_thread().name)
    return {"message": "payment completed"}


@app.get("/profile")
def profile():
    # print("PROFILE called:", threading.current_thread().name)
    return {"message": "profile loaded"}
