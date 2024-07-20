from flask import Flask, render_template


app = Flask(__name__)

@app.route("/")
def chart():
    labels = ["January","February","March","April","May","June","July","August"]
    values = [10,9,8,7,6,4,7,8]
    x = [1, 2, 3, 4, 5]
    y = [10, 8, 6, 4, 2]
    return render_template('index.html', values=values, labels=labels, x=x, y=y)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)