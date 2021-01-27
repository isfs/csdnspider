'''
导入所需要的库
'''
import lxml.etree as le
from URLConn import URLConn
import pymysql
from urllib.request import urlretrieve
from pyecharts import options
# 代入柱状图
from  pyecharts.charts import Bar

d_d=[]
t_t=[]
# 对数据进行整合，变成柱状图，日浏览和月浏览，使用pyecharts方法
def show(data,time,blogID):
    c = Bar()
    for i in range(len(time)):
        time[i] = time[i][:10]
    d = {}
    for i in range(len(time)):
        if time[i] not in d:
            d[time[i]] = 0
        d[time[i]] += int(data[i])
    times=[]
    datas=[]
    for key,value in d.items():
        times.append(key)
        datas.append(value)
    # 将日期数据作为x轴数据
    c.add_xaxis(times)
    # 将访问量数据作为y轴数据,标签为访问量
    c.add_yaxis('访问量', datas)
    # 添加主标题和副标题 ,设置x轴旋转角度为-40度
    subtitle = blogID+'的博客日访问量'
    title = blogID+'访问量柱形图'
    c.set_global_opts(title_opts=options.TitleOpts(title=title, subtitle=subtitle),
                      xaxis_opts=options.AxisOpts(axislabel_opts=options.LabelOpts(rotate=-50)))
    # 渲染生成Html文件
    path = 'templates/'+blogID+'day.html'
    c.render(path)
    print('图形绘制完毕')


    e = Bar()
    for i in range(len(times)):
        times[i] = times[i][:7]
    d = {}
    for i in range(len(times)):
        if times[i] not in d:
            d[times[i]] = 0
        d[times[i]] += int(data[i])
    times = []
    datas = []
    for key, value in d.items():
        times.append(key)
        datas.append(value)
    e.add_xaxis(times)
    e.add_yaxis('访问量', datas)
    subtitle = blogID + '的博客月访问量'
    e.set_global_opts(title_opts=options.TitleOpts(title=title, subtitle=subtitle),
                      xaxis_opts=options.AxisOpts(axislabel_opts=options.LabelOpts(rotate=-40)))
    # 渲染生成Html文件
    path = 'templates/' + blogID + 'month.html'
    e.render(path)
    print('图形绘制完毕')





# 得到每一个博客的链接

def get_href_list(blogID, response):
    href_s = le.HTML(response).xpath('//div[@class="articleMeList-integration"]/div[2]/div/h4/a/@href')     # 博客链接
    title = le.HTML(response).xpath('//div[@class="articleMeList-integration"]/div[2]/div/h4/a/text()')     # 博客标题
    readCount = le.HTML(response).xpath('//div[@class="articleMeList-integration"]/div[2]/div/div[1]/p/span[2]/text()') # 博客访问量
    time = le.HTML(response).xpath('//div[@class="articleMeList-integration"]/div[2]/div/div[1]/p/span[1]/text()') # 博客发布时间
    notes = le.HTML(response).xpath('//div[@class="articleMeList-integration"]/div[2]/div/p/text()')    # 博客简介
    totallist = []  # 总的数据
    # 对数据的清理
    title = [x.strip() for x in title if x.strip() != '']
    notes = [x.strip() for x in notes if x.strip() != '']
    if len(title) == 0:     # 如果未找到信息则说明所有的博客都爬完了
        return False
    # 数据加入数据表中
    for i in range(0, len(href_s)):
        list = []
        list.append(title[i].strip())
        list.append(readCount[i])
        list.append(time[i])
        list.append(href_s[i])
        list.append(blogID)
        list.append(notes[i])
        totallist.append(list)
        d_d.append(readCount[i])
        t_t.append(time[i])
    conn = pymysql.connect(
        host='127.0.0.1',  # 连接ip
        port=3306,  # 端口号
        user='root',  # 数据库用户名
        passwd='123456',  # 数据库密码
        db='blogdata',  # 数据库名
        charset='utf8'  # 设置了数据库的字符集
    )
    # 存入数据库
    cursor = conn.cursor()
    for item in totallist:
        insert1 = "INSERT INTO datas(blogname,pageview,times,bloglink,datas_id,notes) VALUES(%s,%s,%s,%s,%s,%s)"
        value = (item[0], item[1], item[2], item[3], item[4],item[5])
        cursor.execute(insert1, value)
        conn.commit()
    cursor.close()
    conn.close()
    return True

# 对博主数据表的增加
def update(blogID, original, totalrank, totalview, imgsrc, name,point,etc,collect):
    conn = pymysql.connect(
        host='127.0.0.1',  # 连接ip
        port=3306,  # 端口号
        user='root',  # 数据库用户名
        passwd='123456',  # 数据库密码
        db='blogdata',  # 数据库名
        charset='utf8'  # 设置了数据库的字符集
    )
    cursor = conn.cursor()
    insert1 = "INSERT INTO bloggers(bloggername,original,totalrank,totalview,imgsrc,name,point,etc,collect) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    s = 'static/img/'+blogID+'.png'
    urlretrieve(imgsrc, s)
    value = (blogID, original, totalrank, totalview, imgsrc, name,point,etc,collect)
    cursor.execute(insert1, value)
    conn.commit()
    cursor.close()
    conn.close()


def main(blogID):
    # 防止ip被封，同时获取当前页面的html代码
    urlConn = URLConn()
    # 获取博主主页链接
    try:
        link = 'https://blog.csdn.net/{blogID}/article/list/{pages}'.format(blogID=blogID, pages=1)
        html = urlConn.getData(path=link)
    except Exception as e:
        # 表示没有这个博主
        print(e)
        return False
    # 使用lxml中的xpth进行数据的分析
    original = le.HTML(html).xpath('//div[@class="data-info d-flex item-tiling"]/dl[1]/a/dt/span/text()')[0]    # 原创文章
    totalrank = le.HTML(html).xpath('//div[@class="data-info d-flex item-tiling"]/dl[3]/a/dt/span/text()')[0]   # 总排名
    totalview = le.HTML(html).xpath('//div[@class="data-info d-flex item-tiling"]/dl[4]/dt/span/text()')[0]     # 总访问量
    imgsrc = le.HTML(html).xpath('//div[@id="asideProfile"]/div[1]/div[1]/a/img/@src')[0]       # 头像链接
    name = le.HTML(html).xpath('//div[@id="asideProfile"]/div[1]/div[2]/div[1]/a/span/text()')[0]   # 博主昵称
    point = le.HTML(html).xpath('//div[@id="asideProfile"]/div[4]/dl/dt/span/text()')[0]    # 积分
    etc = le.HTML(html).xpath('//div[@id="asideProfile"]/div[4]/dl[2]/dt/span/text()')[0]   # 粉丝数
    collect = le.HTML(html).xpath('//div[@id="asideProfile"]/div[4]/dl[5]/dt/span/text()')[0]   # 收藏数
    update(blogID, original, totalrank, totalview, imgsrc, name,point,etc,collect)
    # sql.createTable()
    # 对该博主的所有页面进行爬取
    try:
        for pages in range(1, 100):
            # 该页面的html
            response = urlConn.getData(
                path='https://blog.csdn.net/{blogID}/article/list/{pages}'.format(blogID=blogID, pages=pages))
            print('开始获取第{id}页数据:'.format(id=pages))
            if get_href_list(blogID, response):
                continue
            else:
                break
    except Exception as e:
        print(e)
    # 图表绘制
    show(d_d,t_t,blogID)
    print("爬取完成")
    return True


# if __name__ == '__main__':
#     main('acm123456789ctf')
#     pass
