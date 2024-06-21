from time import sleep
from plyer import gps


def main():
    gps.configure(on_location=lambda **kwargs: print(f"Location: {kwargs}"))
    gps.start(minTime=5000, minDistance=0)

    while True:
        sleep(1)


if __name__ == '__main__':
    main()
