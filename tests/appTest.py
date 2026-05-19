from flask import Flask, request, make_response

appTest = Flask(__name__)

""" 根目录 """
@appTest.route('/')
def index():
    return 'Hello World!'

""" 传入无类型参数 """
@appTest.route('/hello_name/<name>')
def hello_name(name):
    return 'Hello %s!' % name

""" 传入指定类型参数 """
@appTest.route('/show_blog/<int:post_id>')
def show_blog(post_id):
    return "Blog Number %d" % post_id

""" 设置cookie"""
@appTest.route('/set_cookie')
def set_cookie():
    resp = make_response("success")
    resp.set_cookie("cookie", "value", max_age=3600)
    return resp

@appTest.route('/get_cookie')
def get_cookie():
    return request.cookies.get("cookie")

@appTest.route('/delete_cookie')
def delete_cookie():
    resp = make_response("del_cookie")
    resp.delete_cookie("cookie")
    return resp


if __name__ == '__main__':
    """
    :param host: 主机，默认0.0.0.0
    :param port: 端口，默认5000
    :param debug: 是否debug
    :options
    """
    appTest.run(host='127.0.0.1', port=5000, debug=True, threaded=True)