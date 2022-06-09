import eel

eel.init('web') 

@eel.expose 
def recv_data(question):
    if question != "": 
        answer = "Я понял"
        print(f"[Вы]: {question}")
        print(f"[Бот]: {answer}")
        return answer




eel.start("index.html", size=(700, 700), position=(650,400))