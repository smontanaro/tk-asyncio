#!/usr/bin/env python3

"Testing the idea of providing an off-the-shelf Tk event loop for asyncio"

import asyncio
import random
from tkinter import Tk, Button

class AsyncTk(Tk):
    "Basic Tk with an asyncio-compatible event loop"
    def __init__(self):
        super().__init__()
        self.running = True
        self.runners = [self.tk_loop()]
        self.button_presses = []

    async def tk_loop(self):
        "asyncio 'compatible' tk event loop?"
        # Is there a better way to trigger loop exit than using a state vrbl?
        while self.running:
            self.update()
            await asyncio.sleep(0.05) # obviously, sleep time could be parameterized
            if len(self.button_presses) > 0:
                await self.button_presses.pop(0)

    def stop(self):
        self.running = False

    async def run(self):
        await asyncio.gather(*self.runners)
        
    def add_button_coro(self, coro):
        task = asyncio.create_task(coro)
        self.button_presses.append(task)


class App(AsyncTk):
    "User's app"
    def __init__(self):
        super().__init__()
        self.create_interface()
        self.runners.append(self.counter())

    def create_interface(self):
        b1 = Button(master=self, text='Random Float',
                    command=lambda: print("your wish, as they say...", random.random()))
        b1.pack()
        b2 = Button(master=self, text='Quit', command=self.stop)
        b2.pack()
        b3 = Button(master=self, text='Foo', command=lambda: self.add_button_coro(self.foo()))
        b3.pack()

    async def counter(self):
        "sample async worker... (with apologies to Lawrence Welk)"
        i = 1
        while self.running:
            print("and a", i)
            await asyncio.sleep(1)
            i += 1
            
    async def foo(self):
        print(f"IO task foo has started")
        await asyncio.sleep(1)
        print(f"IO task foo has finished")

async def main():
    app = App()
    await app.run()

if __name__ == '__main__':
    asyncio.run(main())
