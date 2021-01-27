from flask import Flask, redirect, url_for, request, render_template
import settings
import pymysql
import spiderdata

app = Flask(__name__)
app.config.from_object(settings) # 方便debug的设置
# 用pymysql链接数据库
conn = pymysql.connect(
    host='127.0.0.1',  # 连接ip
    port=3306,  # 端口号
    user='root',  # 数据库用户名
    passwd='123456',  # 数据库密码
    db='blogdata',  # 数据库名
    charset='utf8'  # 设置了数据库的字符集
)

# 初始页面
@app.route('/')
def index():
    return render_template('index.html')

# 进入博主的页面
@app.route('/index', methods=['POST', 'GET'])
def gotonext():
    if request.method == 'POST':
        user = request.form['name']
        return redirect(url_for('show', blogname=user))
    else:
        user = request.args.get('name')
        return redirect(url_for('show', blogname=user))


@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        key = request.form['key']
        bloggername = request.form['bloggername']
        return redirect(url_for('show', blogname=bloggername, key=key))
    else:
        return render_template('error.html')


# 日浏览量和月浏览量的图标的展示
@app.route('/graph_day',methods=['POST','GET'])
def graph_day():
    if request.method == 'POST':
        user = request.form['name']
        return render_template(user+'day.html')
    else:
        user = request.args.get('name')
        return render_template(user+'day.html')

@app.route('/graph_month',methods=['POST','GET'])
def graph_month():
    if request.method == 'POST':
        user = request.form['name']
        return render_template(user+'month.html')
    else:
        user = request.args.get('name')
        return render_template(user+'month.html')

# 更新数据后跳转到show页面
@app.route('/update/<blogname>')
def update(blogname):
    sql = "Delete from bloggers where bloggername='{0}'".format(blogname)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    spiderdata.main(blogname)
    cursor.execute("SELECT * FROM bloggers")
    results = cursor.fetchall()
    tmp = get_data(results, blogname, cursor)
    return render_template('show.html', datas=tmp[0], blog=tmp[1], img_src=tmp[2], sortres=tmp[3], update_src=tmp[4], search=(),flag=0)


# 各个博主的主页面的展示
@app.route('/show/<blogname>')
def show(blogname):
    cursor = conn.cursor()
    sql = "SELECT * FROM bloggers"
    cursor.execute(sql)
    conn.commit()
    results = cursor.fetchall()
    # 如果该博主存在数据库中则直接显示出其数据
    if any(blogname in i for i in results):
        key = request.args.get("key")
        tmp = get_data(results, blogname, cursor)
        results =()
        flag = 0
        if key != None:
            sql = "SELECT * FROM datas WHERE  datas_id='{0}' AND blogname like '%{1}%'".format(blogname,key)
            cursor.execute(sql)
            conn.commit()
            results = cursor.fetchall()
            flag = 1
        return render_template('show.html', datas=tmp[0], blog=tmp[1], img_src=tmp[2], sortres=tmp[3], update_src=tmp[4],search=results,flag=flag)
    else:
        # 否则的话爬取一遍数据
        if spiderdata.main(blogname)==False:
            # 如果该博主在csdn中不存在，则返回error页面
            return render_template('error.html')
        cursor.execute(sql)
        results = cursor.fetchall()
        tmp = get_data(results, blogname, cursor)
        return render_template('show.html', datas=tmp[0], blog=tmp[1], img_src=tmp[2], sortres=tmp[3], update_src=tmp[4],search=(),flag=0)

# 数据按访问量进行排序
def takeElem(elem):
    return int(elem[2])

# 得到该博主的数据
def get_data(results, blogname, cursor):
    for item in results:
        if item[0] == blogname:
            sql1 = "SELECT * FROM datas WHERE datas_id='{0}'".format(blogname)
            cursor.execute(sql1)
            results = cursor.fetchall()
            res = list(results)
            res.sort(key=takeElem, reverse=True)
            img_src = '../static/img/' + item[0] + '.png'
            update_src = "http://localhost:5000/update/" + blogname
            return (results, item, img_src, res,update_src)


if __name__ == '__main__':
    app.run()
