import asyncio

async def nested(id : int = 0):
    print(f'NESTED {id}: in')
    for i in range(10):
        print(f'NESTED {id}: doing things...', i)
        await asyncio.sleep(1)
    print(f'NESTED {id}: out')
    return 

async def main():
    print('MAIN: in')
    async with asyncio.TaskGroup() as tg:
        tg.create_task(nested(1))
        tg.create_task(nested(2))
        tg.create_task(nested(3))
    print('MAIN: out')

asyncio.run(main())