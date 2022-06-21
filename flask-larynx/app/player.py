from tempfile import NamedTemporaryFile
from time import sleep

import pygame

pygame.mixer.init()


def play(wav: bytes) -> None:
    with NamedTemporaryFile("wav", "rb") as fp:
        fp.write(wav)
        fp.flush()
        pygame.mixer.music.load(fp.name)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            sleep(0.01)
