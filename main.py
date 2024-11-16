import asyncio
import random
import time
import datetime

"""
메인코루틴이 있고, 3개의 서브코루틴이 있음.

메인코루틴은 서버처럼 입력을 담당하고, 3개의 서브코루틴은 자신에게 온 입력에 대한 처리를 진행함.
이걸 EventLoop 기반인 asyncio로 구현하고 싶었는데 잘 안되던 부분이 있었음.

바로, 메인코루틴이 원인이었는데 메인 코루틴에서 sleep 없이 만들 경우 메인코루틴이 계속 실행되면서
서브코루틴이 실행될 기회가 없어서 전혀 실행되지 않음.

while문을 한번 돌고 다음 코루틴으로 실행을 넘길 줄 알았지만 전혀 그렇게 작동하지 않았음을 이번
예제로 깨닫게 됨.
"""


class ServerState:
    def __init__(self, sid: int):
        self.sid = sid
        self.queue = asyncio.Queue()
        self.worker_task = None

    async def worker(self):
        print("worker 실행됨.")
        while True:
            sleep_timer = await self.queue.get()  # 작업 대기
            await asyncio.sleep(sleep_timer)
            print(f"{datetime.datetime.now()} server {self.sid}: sleep {sleep_timer}s (remain:{self.queue})")
            self.queue.task_done()


async def main():
    server_cnt = 3
    server_task = [ServerState(i + 1) for i in range(server_cnt)]
    for server in server_task:
        # await 없이 task를 생성해야 기다리지 않고 별도의 서브코루틴으로서 작동함.
        asyncio.create_task(server.worker())

    start_time = time.time()
    tasks = []
    with open("task.txt", "r", encoding="utf-8") as f:
        tasks.extend(list(map(lambda x: x.split(","), f.readlines())))

    task_idx = 1
    while True:
        if task_idx >= len(tasks):
            await asyncio.sleep(0.1)
            continue
        created_at, server = tasks[task_idx]

        current_time = time.time()
        diff = current_time - start_time

        if diff < int(created_at):
            # sleep이 코루틴의 break point로 sleep되는 동안 다른 코루틴이 작동될 수 있다.
            await asyncio.sleep(0.1)
            continue

        task_idx += 1
        target_server = server_task[int(server)]
        sleep_timer = random.uniform(0.1, 10.0)
        await target_server.queue.put(sleep_timer)
        print(f"{datetime.datetime.now()} server {target_server.sid}: create_task(sleep:{sleep_timer}s)")

if __name__ == "__main__":
    asyncio.run(main())

