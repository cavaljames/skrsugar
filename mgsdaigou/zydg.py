"""
@File    :   zydg.py    
@Contact :   zhangyu@onesight.com

@Modify Time    @Author @Version    @Description
------------    ------- --------    -----------
2022/1/4         zhangyu 1.0         None
"""
from flask import Flask, render_template, request, session, redirect
from modules import config
from modules import common
from modules.common import rds
import re

app = Flask(__name__)
app.secret_key = 'SECRETKEY'
app._static_folder = "./static"
app.config['DEBUG'] = True


@app.route('/index')
def index():
    user_info = session.get('user_info')
    if not user_info:
        return redirect('/login')
    datas = []
    for k in rds.keys():
        d = rds.hgetall(k)
        d['link'] = k
        print(k)
        try:
            d['name'] = re.search(r'.+\/([\w|\-]+)\.html', k).group(1) if re.search(r'', k) else d['title']
        except Exception as ex:
            print(ex)
            d['name'] = k
        datas.append(d)
    sorted_data = sorted(datas, key=lambda v: int(v['index']))
    print(sorted_data)
    return render_template('index.html', datas=sorted_data)


@app.route('/login', methods=['GET', "POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    user = request.form.get('username')
    pwd = request.form.get('password')
    if user == 'sugar' and pwd == 'sugardaddy156':
        session['user_info'] = user
        return redirect('/index')
    else:
        return render_template('login.html', msg='用户名或密码输入错误')


@app.route('/logout')
def logout_():
    del session['user_info']
    return redirect('login')


if __name__ == '__main__':
    common.get_thumbnails(config.ZYDG_HOMEPAGE, 5)
    h = '0.0.0.0'
    app.run(host=h, port=7799, debug=True, use_reloader=False)
