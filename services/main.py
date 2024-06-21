from jnius import autoclass

PythonService = autoclass('org.kivy.android.PythonService')
service = PythonService.mService

def start():
    from myservice import main
    main()

if __name__ == "__main__":
    start()
