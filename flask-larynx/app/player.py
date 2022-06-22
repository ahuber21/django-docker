from tempfile import NamedTemporaryFile
from time import sleep

import pygame

pygame.mixer.pre_init(buffer=1512)
pygame.mixer.init()


def play(wav: bytes) -> None:
    with NamedTemporaryFile("wav", "rb") as fp:
        fp.write(wav)
        fp.flush()
        pygame.mixer.music.load(fp.name)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            sleep(0.01)


if __name__ == "__main__":
    # downloaded from https://www.kozco.com/tech/piano2-Audacity1.2.5.mp3
    pygame.mixer.music.load("piano2-Audacity1.2.5.mp3")
    print("Audio loaded")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        sleep(0.1)
    print("Successfully played the file")
