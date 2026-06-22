import asyncio
import time
import httpx


async def call_url(client, name, url):
    start = time.time()
    print(f"{name} started")

    response = await client.get(url, timeout=60)

    end = time.time()
    print(f"{name} finished in {end - start:.2f}s -> {response.json()}")


async def main():
    async with httpx.AsyncClient() as client:
        # Start 2 payment requests first
        task1 = asyncio.create_task(
            call_url(client, "payment-1", "http://127.0.0.1:8000/payment")
        )

        task2 = asyncio.create_task(
            call_url(client, "payment-2", "http://127.0.0.1:8000/payment")
        )

        # Wait 1 second, then call profile
        await asyncio.sleep(1)

        task3 = asyncio.create_task(
            call_url(client, "profile", "http://127.0.0.1:8000/profile")
        )

        await asyncio.gather(task1, task2, task3)


asyncio.run(main())