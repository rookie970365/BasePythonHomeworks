from fastapi import FastAPI
from view import router as view_router

app = FastAPI()
app.include_router(view_router)


@app.get("/")
def root():
    return {"message": "Homework_03"}


@app.get("/fibo")
def fibo(n: int):
    lst = [0, 1]
    for i in range(2, n + 1):
        lst.append(lst[i - 1] + lst[i - 2])
    return {f"ряд фибоначчи из {n} элементов": lst}
