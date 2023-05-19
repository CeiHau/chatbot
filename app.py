from flask import Flask, render_template, request, jsonify
import bot
app = Flask(__name__)

# default context
default_context = "Kanye West initially made his mark on the music industry as a producer for leading artists. He showcased his own abilities as a rapper with his 2004 debut, College Dropout, and cemented his place atop the hip hop world via such chart-topping albums as Late Registration (2005), My Beautiful Dark Twisted Fantasy (2010), Yeezus (2013) and Ye (2018). The winner of nearly two dozen Grammy Awards, West is also known for his awards-show theatrics, forays into fashion and marriage to Kim Kardashian."
bot = bot.Bot(default_context)


@app.get("/")
def show():
    return render_template("base.html")



@app.post("/chat")
def chat():
    r = request.get_json()
    print(type(r), r)
    if "message" in r:
        question = request.get_json().get("message")
        response = bot.ask(question)

        print(response)

    message = {"answer": response}
    return jsonify(message)

@app.post("/context")
def setContext():
    context = request.get_json().get("context")
    bot.changeContext(context)
    response = "Set a new context, please ask question"
    message = {"answer": response}
    return jsonify(message)



if __name__ == "__main__":
    app.run(debug=True)

