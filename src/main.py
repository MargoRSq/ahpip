import uvicorn

from src import app


def main():
    # webbrowser.open("http://localhost:8000/work/first")
    uvicorn.run(app)


main()
