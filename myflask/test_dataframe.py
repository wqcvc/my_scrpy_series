from flask import Flask, request, render_template, session, redirect
import numpy as np
import pandas as pd


app = Flask(__name__)

df = pd.DataFrame({'A': [0, 1, 2, 3, 4],
                   'B': [5, 6, 7, 8, 9],
                   'C': ['a', 'b', 'c--', 'd', 'e']})


@app.route('/', methods=("POST", "GET"))
def html_table():

    return render_template('simple.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)



if __name__ == '__main__':
    app.run(debug= True)