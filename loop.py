import asyncio


loop = asyncio.get_event_loop()
loop_hash = hash(loop)
loop2 = None
loop2_hash = None


async def main():
    global loop2, loop2_hash
    loop2 = asyncio.get_event_loop()
    loop2_hash = hash(loop2)
    print(f"main()")
    print(f"loop : {loop_hash}")
    print(f"loop2 : {loop2_hash}")
    print(f"is same : {loop_hash == loop2_hash}")
    print(f"loop is close : {loop.is_closed()}")
    print(f"loop2 is close : {loop2.is_closed()}")
    print(f"loop is running : {loop.is_running()}")
    print(f"loop2 is running : {loop2.is_running()}")


async def main2():
    print(f"main2()")
    print(f"loop : {loop_hash}")
    print(f"loop2 : {loop2_hash}")
    print(f"is same : {loop_hash == loop2_hash}")
    print(f"loop is close : {loop.is_closed()}")
    print(f"loop2 is close : {loop2.is_closed()}")
    print(f"loop is running : {loop.is_running()}")
    print(f"loop2 is running : {loop2.is_running()}")


if __name__ == "__main__":
    asyncio.run(main())
    loop.run_until_complete(main2())

"""
asyncio.run()의 doc string 내용을 읽어보면, `This function always creates a new event loop and closes it at the end.`
run 함수를 사용할 경우, 항상 새로운 Event Loop를 생성하고 마지막에 종료된다고 명시되어 있습니다.

그래서, loop = asyncio.get_event_loop()로 미리 얻은 loop와 asyncio.run에서 실행중인 loop는 서로 다른 loop가 됩니다.
EventLoop는 Thread당 하나씩만 돌릴 수 있고, loop를 직접 관리하고 싶다면 loop.run_until_complete로 해당 루프로 돌리는 방식으로 선택.
"""