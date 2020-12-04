from flask import Flask, escape, url_for, redirect, request, render_template, make_response, session
from werkzeug.utils import secure_filename
import os
app = Flask(__name__)


# # 1.开始
# @app.route('/')
# def hello_world():
#     return 'hello world...'

# 2.路径
# @app.route('/')
# def index():
#     return 'index page change.'


@app.route('/world')
def hello_world():
    return 'hello world.'


# 3.变量规则: 传递参数
# 转换器类型: string int float path uuid
@app.route('/uuu/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'uuu %s' % escape(username)


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % escape(subpath)


# 4.url构建
# url_for()

# 5.路由 ---不知道为啥不生效
# def test_add_url():
#     return "test add url ..."
#
# app.add_url_rule('/', endpoint='test', view_func=test_add_url)


# 6. URL构建
# redirect:重定向
@app.route('/admin')
def hello_admin():
    return f"hello Admin"

@app.route('/guest/<guest>')
def hello_guest(guest):
    return f"hello [{guest}] as Guest."

@app.route('/user/<name>')
def hello_user(name):
    if name == 'admin':
        return redirect(url_for('hello_admin'))
    else:
        return redirect(url_for('hello_guest',guest = name))


# 7.http方法: get post delete head put
# 使用方式: 打开login.html
# request方法: 前后端交互
# Form - 它是一个字典对象，包含表单参数及其值的键和值对。
# args - 解析查询字符串的内容，它是问号（？）之后的URL的一部分。
# Cookies  - 保存Cookie名称和值的字典对象。
# files - 与上传文件有关的数据。
# method - 当前请求方法。
@app.route('/success/<name>')
def success(name):
    return f"welcome {name}"

# @app.route('/login',methods=['POST','GET'])
# def login():
#     if request.method == 'POST':
#         user = request.form['nm']
#         return redirect(url_for('success',name = user))
#     else:
#         user = request.args.get('nm')
#         return redirect(url_for('success',name = user))

# 8.Flask模版
# 视图函数只负责业务逻辑和数据处理(业务逻辑方面) Jinja2
# 而模板则取到视图函数的数据结果进行展示(视图展示方面)
# 代码结构清晰,耦合度低
# render_template
# 模版存放在 templates目录
# 9.静态文件
# css js等 存放在 static目录
# @app.route('/')
# def index():
#     my_str = 'my_str is string'
#     my_int = 125
#     my_dict = {1:'xxx'}
#     my_list = [1,2,3,4,5]
#     return render_template('hello.html',my_dict=my_dict,my_int=my_int,my_str=my_str,my_list=my_list)

# 10. 表单数据发送
# html中的 action 绑定 url
@app.route('/student')
def student():
   return render_template('student.html')


@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      return render_template("result.html", result = result)

# 11. cookies
@app.route("/set_cookies")
def set_cookie():
    resp = make_response("success")
    resp.set_cookie("w3cshool", "w3cshool",max_age=3600)
    return resp

@app.route("/get_cookies")
def get_cookie():
    cookie_1 = request.cookies.get("w3cshool")  # 获取名字为Itcast_1对应cookie的值
    return cookie_1

@app.route("/delete_cookies")
def delete_cookie():
    resp = make_response("del success")
    resp.delete_cookie("w3cshool")

    return resp


# 11.Flask 会话： session
app.secret_key = 'fkdjsafjdkfdlkjfadskjfadskljdsfklj'


# @app.route('/')
# def index():
#     if 'username' in session:
#         username = session['username']
#         return '登录用户名是:' + username + '<br>' + "<b><a href = '/logout'>点击这里注销</a></b>"
#     return "您暂未登录， <br><a href = '/login'></b>" + "点击这里登录</b></a>"
#
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         session['username'] = request.form['username']
#         return redirect(url_for('index'))
#     return '''
#    <form action = "" method = "post">
#       <p><input type ="text" name ="username"/></p>
#       <p><input type ="submit" value ="登录"/></p>
#    </form>
#    '''
#
# @app.route('/logout')
# def logout():
#    # remove the username from the session if it is there
#    session.pop('username', None)
#    return redirect(url_for('index'))


# 12. 重定向和错误
# redirect + abort(404)

# 13. 消息闪现
# flash(message, category)
# get_flashed_messages(with_categories, category_filter)

# 14. 文件上传
app.config['UPLOAD_FOLDER'] = 'upload/'


@app.route('/upload')
def upload_file():
   return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
   if request.method == 'POST':
      f = request.files['file']
      f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
      return 'file uploaded successfully'


# 15.Flask扩展
# from flask_sqlalchemy import SQLAlchemy
# ...mail WTF Sijax ...

if __name__ == "__main__":
    # debug开启 自动重新加载改动
    app.debug = True
    app.run()  # or app.run(debug=True)





"""
启动：
export FLASK_APP=main.py
flask run / flask run --host=0.0.0.0
停止：
ctrl + c
再次启动：
lsof -i:5000
kill PID
"""
