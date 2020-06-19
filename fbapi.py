from flask import Flask
app = Flask(__name__)
from flask import request
from livereload import Server

from scrapper.facebook import FaceBook as fb

@app.route('/api')
def fbapi():
    url = request.args.get('user')
    res = fb.getInstance().parse()
    return res

@app.route("/about")
def about():
    return "About page"
# @app.route('/api',methods = ['POST', 'GET'])
# def fbapi():
#    if request.method == 'POST':
#       user = request.form['url']
#       return redirect(url_for('success',name = user))
#    else:
#       user = request.args.get('url')
#       return redirect(url_for('success',name = user))
if __name__ == '__main__':
    app.run(debug=True)