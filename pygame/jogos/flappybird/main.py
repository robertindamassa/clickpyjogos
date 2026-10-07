import asyncio
import pygame as pg
from game import Game

async def main():
    game = Game()
    await game.gameLoop()

if __name__ == "__main__":
    asyncio.run(main())
