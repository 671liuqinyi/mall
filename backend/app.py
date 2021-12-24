import datetime
import time
import traceback
import pymysql
from flask import Flask
from flask import request

app = Flask(__name__)


dbhost = "localhost"
dbname = "mall"

# 服务器数据库参数
# dbuser = "lqy"
# dbpassword = "671"

# 本地数据库参数
dbuser = "root"
dbpassword = "671jiayou"




# 用户登录
@app.route('/api/userlogin', methods=["post"])
def UserLogin():
    # 把用户名和密码注册到数据库中
    data = request.get_json(silent=True)
    username = data['username']
    password = data['password']
    # 连接数据库,此前在数据库中创建数据库TESTDB
    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbname)
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 插入语句
    sql = "select * from user where login_name = '" + username + "' and password = '" + password + "'"
    # sql = "select * from user where password = '" + password + "'"
    # print(sql)
    role = ''
    userid = ''
    username = ''
    try:
        # 执行sql语句
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res[0][4])
        if len(res) == 1:
            code = '200'
            userid = res[0][0]
            username = res[0][2]
            role = res[0][4]
        else:
            code = '404'
        # 提交到数据库执行
        db.commit()
    except:
        code = '404'
        # 抛出错误信息
        traceback.print_exc()
        # 如果发生错误则回滚
        db.rollback()

    # 关闭数据库连接
    db.close()
    return {"code": code, "data": {"userid": userid, "username": username, "role": role}}


# 用户注册
@app.route('/api/userregister', methods=["post"])
def UserRegister():
    data = request.get_json(silent=True)
    username = data['username']
    password = data['password']
    print(password)
    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbname)
    code = '200'
    try:
        cursor = db.cursor()
        sql = "select * from user where login_name= '" + username + "'"
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(len(res))
        if len(res) != 0:
            code = '201'
        else:
            if password == '':
                code = '404'
                return {"code": code, "data": ''}
            cursor1 = db.cursor()
            sql1 = "select * from user"
            cursor1.execute(sql1)
            res1 = cursor1.fetchall()
            number = len(res1) + 1
            # print("number ", number)

            cursor2 = db.cursor()
            sql2 = "INSERT INTO user(user_id,login_name, password,role) VALUES (" + str(
                number) + " ,'" + username + "','" + password + "',3)"
            # print(sql2)
            cursor2.execute(sql2)
            db.commit()
            code = '200'
    except:
        code = '404'
    # 关闭数据库连接
    db.close()
    return {"code": code, "data": ''}


# 查询首页商品
@app.route('/api/getproduct', methods=["get"])
def GetProduct():
    Type = request.args.get("type")

    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbname)
    cursor = db.cursor()
    sql = ''
    sql1 = "select goods_category_id, goods_id,goods_intro, goods_name,stock_num, goods_cover_img,original_price,selling_price"
    sql1 += " from goods_info where goods_category_id in ('46','47') limit 100"

    sql2 = "select goods_category_id, goods_id,goods_intro, goods_name,stock_num, goods_cover_img,original_price,selling_price"
    sql2 += " from goods_info where goods_category_id in ('0','86') limit 100"

    sql3 = "select goods_category_id, goods_id,goods_intro, goods_name,stock_num, goods_cover_img,original_price,selling_price"
    sql3 += " from goods_info where goods_category_id in ('46','47','51') limit 100"
    if Type == 'phone':
        sql = sql1
    elif Type == 'dailygoods':
        sql = sql2
    try:
        # 执行sql语句
        cursor.execute(sql)
        result = cursor.fetchall()
        # print('result ',len(result))
        res = []
        for item in result:
            category_id = item[0]
            product_id = item[1]
            product_intro = item[2]
            product_name = item[3]
            product_num = item[4]
            product_picture = item[5]
            product_price = item[6]
            product_selling_price = item[7]
            product_title = product_intro
            temp = {"category_id": category_id, "product_id": product_id, "product_intro": product_intro,
                    "product_name": product_name, "product_num": product_num, "product_picture": product_picture,
                    "product_price": product_price, "product_selling_price": product_selling_price,
                    "product_title": product_title}
            res.append(temp)
        code = '200'

    except:
        # 如果发生错误则回滚
        traceback.print_exc()
        db.rollback()
        code = '404'
        res = []
    # 关闭数据库连接
    db.close()
    return {'code': code, 'data': res}


# 面包屑切换查询商品
@app.route('/api/getallproduct', methods=["post"])
def GetAllProduct():
    data = request.get_json(silent=True)
    categoryID = data['categoryID']
    # print("categoryID ",categoryID[0])
    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbname)
    cursor = db.cursor()
    sql = ''
    sql1 = "select goods_category_id, goods_id,goods_intro, goods_name,stock_num, goods_cover_img,original_price,selling_price"
    sql1 += " from goods_info where goods_category_id in ('46','47') limit 100"

    sql2 = "select goods_category_id, goods_id,goods_intro, goods_name,stock_num, goods_cover_img,original_price,selling_price"
    sql2 += " from goods_info where goods_category_id in ('0','86') limit 100"

    sql3 = "select goods_category_id, goods_id,goods_intro, goods_name,stock_num, goods_cover_img,original_price,selling_price"
    sql3 += " from goods_info where goods_category_id in ('46','47','51') limit 200"
    if categoryID[0] == 0:
        sql = sql3
        total = 200
    elif categoryID[0] == 1:
        sql = sql1
        total = 100
    elif categoryID[0] == 2:
        sql = sql2
        total = 100
    try:
        # 执行sql语句
        cursor.execute(sql)
        result = cursor.fetchall()
        # print('result ',len(result))
        res = []
        for item in result:
            category_id = item[0]
            product_id = item[1]
            product_intro = item[2]
            product_name = item[3]
            product_num = item[4]
            product_picture = item[5]
            product_price = item[6]
            product_selling_price = item[7]
            product_title = product_intro
            temp = {"category_id": category_id, "product_id": product_id, "product_intro": product_intro,
                    "product_name": product_name, "product_num": product_num, "product_picture": product_picture,
                    "product_price": product_price, "product_selling_price": product_selling_price,
                    "product_title": product_title}
            res.append(temp)
        code = '200'

    except:
        # 如果发生错误则回滚
        traceback.print_exc()
        db.rollback()
        code = '404'
        res = []
    # 关闭数据库连接
    db.close()
    return {'code': code, 'data': res, "total": total}


# 搜索商品
@app.route('/api/getproductbysearch', methods=["post"])
def GetProductBySearch():
    data = request.get_json(silent=True)
    search = data['search']
    tempstr = '%'
    for i in search:
        tempstr = tempstr + i + "%"
    search = tempstr
    # print("search ",search)
    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbname)
    cursor = db.cursor()
    sql = "select goods_category_id, goods_id,goods_intro, goods_name,stock_num, goods_cover_img,original_price,selling_price"
    sql += " from goods_info where goods_name like '" + search + "'"
    # print(sql)
    try:
        # 执行sql语句
        cursor.execute(sql)
        result = cursor.fetchall()
        total = len(result)
        # print('result ',len(result))
        res = []
        for item in result:
            category_id = item[0]
            product_id = item[1]
            product_intro = item[2]
            product_name = item[3]
            product_num = item[4]
            product_picture = item[5]
            product_price = item[6]
            product_selling_price = item[7]
            product_title = product_intro
            temp = {"category_id": category_id, "product_id": product_id, "product_intro": product_intro,
                    "product_name": product_name, "product_num": product_num, "product_picture": product_picture,
                    "product_price": product_price, "product_selling_price": product_selling_price,
                    "product_title": product_title}
            res.append(temp)
        code = '200'

    except:
        # 如果发生错误则回滚
        traceback.print_exc()
        db.rollback()
        code = '404'
        total = 0
        res = []
    # 关闭数据库连接
    db.close()
    return {'code': code, 'data': res, "total": total}


# 获得商品详细信息
@app.route('/api/getproductdetails', methods=["post"])
def GetProductDetails():
    data = request.get_json(silent=True)
    productID = data['productID']
    # print("productID ",productID)
    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbname)
    cursor = db.cursor()
    sql = "select goods_category_id, goods_id,goods_intro, goods_name,stock_num, goods_cover_img,original_price,selling_price"
    sql += " from goods_info where goods_id = '" + str(productID) + "'"
    # print(sql)
    try:
        # 执行sql语句
        cursor.execute(sql)
        result = cursor.fetchall()

        # print('result ',len(result))
        res = []
        for item in result:
            category_id = item[0]
            product_id = item[1]
            product_intro = item[2]
            product_name = item[3]
            product_num = item[4]
            product_picture = item[5]
            product_price = item[6]
            product_selling_price = item[7]
            product_title = product_intro
            temp = {"category_id": category_id, "product_id": product_id, "product_intro": product_intro,
                    "product_name": product_name, "product_num": product_num, "product_picture": product_picture,
                    "product_price": product_price, "product_selling_price": product_selling_price,
                    "product_title": product_title}
            res.append(temp)
        code = '200'

    except:
        # 如果发生错误则回滚
        traceback.print_exc()
        db.rollback()
        code = '404'
        total = 0
        res = []
    # 关闭数据库连接
    db.close()
    return {'code': code, 'data': res}


# 查找收藏信息
@app.route('/api/findcollect', methods=["post"])
def FindCollect():
    data = request.get_json(silent=True)
    user_id = data['user_id']
    # print("user_id ",user_id)
    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbname)
    cursor = db.cursor()
    sql = "select likes from user where login_name='" + user_id + "'"
    cursor.execute(sql)
    result = cursor.fetchall()
    # print(result[0][0],type(result[0][0]))
    if result[0][0]==None:
        return {'code': '404', 'data': []}
    result=result[0][0].split(',')
    # print('result ',result,type(result))
    findlist = "('"
    for item in result:
        findlist = findlist + item + "','"
    findlist = findlist[:-2] + ")"
    # print("findlist ",findlist)
    sql1 = "select goods_category_id, goods_id,goods_intro, goods_name,stock_num, goods_cover_img,original_price,selling_price"
    sql1 += " from goods_info where goods_id in " + findlist
    # print("sql1 ",sql1)
    try:
        # 执行sql语句
        cursor1 = db.cursor()
        cursor1.execute(sql1)
        result = cursor1.fetchall()
        # print('result ',len(result))
        res = []
        for item in result:
            category_id = item[0]
            product_id = item[1]
            product_intro = item[2]
            product_name = item[3]
            product_num = item[4]
            product_picture = item[5]
            product_price = item[6]
            product_selling_price = item[7]
            product_title = product_intro
            temp = {"category_id": category_id, "product_id": product_id, "product_intro": product_intro,
                    "product_name": product_name, "product_num": product_num, "product_picture": product_picture,
                    "product_price": product_price, "product_selling_price": product_selling_price,
                    "product_title": product_title}
            res.append(temp)
        code = '200'

    except:
        # 如果发生错误则回滚
        traceback.print_exc()
        db.rollback()
        code = '404'
        total = 0
        res = []
    # 关闭数据库连接
    db.close()
    return {'code': code, 'data': res}


# 增加收藏信息
@app.route('/api/addcollect', methods=["post"])
def AddCollect():
    data = request.get_json(silent=True)
    user_id = data['user_id']
    product_id = str(data['product_id'])
    # print("user_id ",user_id)
    # print("product_id ",product_id,type(product_id))
    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbname)
    cursor = db.cursor()
    sql = "select likes from user where login_name='" + user_id + "'"
    # print("sql ",sql)
    try:
        # 执行sql语句
        cursor.execute(sql)
        result = cursor.fetchall()[0][0]
        if result == None:
            result=[]
        else:
            result=result.split(',')
        # 已收藏商品不能继续添加
        if product_id in result:
            return {"code": '201'}
        result.append(product_id)
        # print('result ',result,type(result))
        newlikes = ''
        for item in result:
            newlikes = newlikes + item + ','
        newlikes = newlikes[:-1]
        # print("newlikes ", newlikes)
        cursor1 = db.cursor()
        sql1 = "update user set likes = '" + newlikes + "' where login_name='" + user_id + "'"
        cursor1.execute(sql1)
        db.commit()
        # print("sql1 ",sql1)
        code = '200'

    except:
        # 如果发生错误则回滚
        traceback.print_exc()
        db.rollback()
        code = '404'
        total = 0
        res = []
    # 关闭数据库连接
    db.close()
    return {'code': code}


# 删除收藏信息
@app.route('/api/deletecollect', methods=["post"])
def DeleteCollect():
    data = request.get_json(silent=True)
    user_id = data['user_id']
    product_id = data['product_id']
    # print("user_id ",user_id)
    # print("product_id ",product_id,type(product_id))
    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbname)
    cursor = db.cursor()
    sql = "select likes from user where login_name='" + user_id + "'"
    # print("sql ",sql)
    try:
        # 执行sql语句
        cursor.execute(sql)
        result = cursor.fetchall()[0][0].split(',')
        result.remove(str(product_id))
        # print('result ',result,type(result))
        newlikes = ''
        for item in result:
            newlikes = newlikes + item + ','
        newlikes = newlikes[:-1]
        # print("newlikes ", newlikes)
        cursor1 = db.cursor()
        sql1 = "update user set likes = '" + newlikes + "' where login_name='" + user_id + "'"
        cursor1.execute(sql1)
        db.commit()
        # print("sql1 ",sql1)
        code = '200'

    except:
        # 如果发生错误则回滚
        traceback.print_exc()
        db.rollback()
        code = '404'
        total = 0
        res = []
    # 关闭数据库连接
    db.close()
    return {'code': code}


# 获取购物车数据
@app.route('/api/getshoppingcart', methods=["post"])
def GetShoppingCart():
    data = request.get_json(silent=True)
    user_id = data['user_id']
    # print("user_id ", user_id, type(user_id))
    # print("product_id ",product_id,type(product_id))
    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbname)
    cursor = db.cursor()
    sql = "select user.user_id, stock_num, goods_count, selling_price, goods_info.goods_id, goods_name,goods_carousel "
    sql += "from user, goods_info, shopping_cart_item "
    sql += "where user.user_id = shopping_cart_item.user_id and shopping_cart_item.goods_id = goods_info.goods_id and "
    sql += "shopping_cart_item.user_id = " + str(user_id)
    # print("sql ", sql)
    try:
        # 执行sql语句
        cursor1 = db.cursor()
        cursor1.execute(sql)
        result = cursor1.fetchall()
        # print('result ',len(result))
        res = []
        for item in result:
            id = item[0]
            maxNum = item[1]
            num = item[2]
            price = item[3]
            productID = item[4]
            productName = item[5]
            productImg = item[6]
            temp = {"check": "true", "id": id, "maxNum": maxNum, "num": num,
                    "price": price, "productID": productID, "productImg": productImg,
                    "productName": productName}
            res.append(temp)
        code = '200'

    except:
        # 如果发生错误则回滚
        traceback.print_exc()
        db.rollback()
        code = '404'
        res = []
    # 关闭数据库连接
    db.close()
    return {'code': code, "data": res}


# 更新购物车数据-商品数量
@app.route('/api/updateshoppingcartnumber', methods=["post"])
def UpdateShoppingCartNumber():
    data = request.get_json(silent=True)
    num = str(data['num'])
    product_id = str(data['product_id'])
    user_id = str(data['user_id'])
    # print("user_id ", user_id, type(user_id))
    # print("product_id ",product_id,type(product_id))
    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbname)
    cursor = db.cursor()
    sql = "update shopping_cart_item set goods_count= " + num + " where user_id=" + user_id + " and goods_id=" + product_id
    # print("sql ",sql)
    try:
        cursor.execute(sql)
        db.commit()
        code = '200'
    except:
        code = '404'
    # 关闭数据库连接
    db.close()
    return {'code': code}


# 增加购物车数据
@app.route('/api/addshoppingcart', methods=["post"])
def AddShoppingCart():
    data = request.get_json(silent=True)
    product_id = str(data['product_id'])
    user_id = str(data['user_id'])
    # print("user_id ", user_id, type(user_id))
    # print("product_id ",product_id,type(product_id))
    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbname)
    cursor = db.cursor()
    sql = "select * from shopping_cart_item where user_id=" + user_id + " and goods_id=" + product_id
    cursor.execute(sql)
    result = cursor.fetchall()
    if len(result) != 0:
        return {'code': '201'}
    # print("sql ",sql)
    try:
        cursor1 = db.cursor()
        sql1 = "insert into shopping_cart_item(user_id, goods_id, goods_count) values(" + user_id + "," + product_id + ",1)"
        cursor1.execute(sql1)
        # print(sql1)
        db.commit()
        code = '200'
    except:
        code = '404'
    # 关闭数据库连接
    db.close()
    return {'code': code}


# 删除购物车数据
@app.route('/api/deleteshoppingcart', methods=["post"])
def DeleteShoppingCart():
    data = request.get_json(silent=True)
    product_id = str(data['product_id'])
    user_id = str(data['user_id'])
    # print("user_id ", user_id, type(user_id))
    # print("product_id ",product_id,type(product_id))
    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbname)
    cursor = db.cursor()
    sql = "delete from shopping_cart_item where user_id=" + user_id + " and goods_id=" + product_id
    # print("sql ",sql)
    try:
        cursor.execute(sql)
        db.commit()
        code = '200'
    except:
        code = '404'
    # 关闭数据库连接
    db.close()
    return {'code': code}


# 获取订单数据
@app.route('/api/getorder', methods=["post"])
def GetOrder():
    data = request.get_json(silent=True)
    user_id = str(data['user_id'])
    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbname)
    cursor = db.cursor()
    sql = "select order_id,order_no,create_time from orders where user_id = "+user_id
    # print("sql ",sql)
    cursor.execute(sql)
    result = cursor.fetchall()
    # print(result,type(result))
    res = []
    for item in result:
        order_id = str(item[0])
        order_no = item[1]
        # order_time = int(time.mktime(time.strptime(str(item[2]), '%Y-%m-%d %H:%M:%S')))
        order_time = str(item[2])

        # print("order_no ",order_no)
        # print("order_time ",order_time)
        #     # datetime 转 时间戳
        #     result =
        cursor1= db.cursor()
        sql1="select order_item.goods_id,goods_info.goods_name,goods_count,goods_info.goods_carousel,"
        sql1+=" goods_info.selling_price"
        sql1+=" from order_item,goods_info where order_item.goods_id = goods_info.goods_id"
        sql1+=" and order_id="+order_id
        # print("sql1,", sql1)
        cursor1.execute(sql1)
        goods=cursor1.fetchall()
        # print("goods ",goods,type(goods))
        temp_order = []
        for good in goods:
            product_id=good[0]
            product_name=good[1]
            product_num=good[2]
            product_picture=good[3]
            product_price=good[4]
            temp_product={"order_id":order_no,"order_time":order_time,"product_id":product_id,
                          "product_name":product_name,"product_num":product_num,"product_picture":product_picture,
                          "product_price":product_price}
            temp_order.append(temp_product)
            # print("good ",good)
        res.append(temp_order)
    # print(res)
    db.close()
    return {"code":'200',"data":res}

# 增加订单数据
@app.route('/api/addorder', methods=["post"])
def AddOrder():
    data = request.get_json(silent=True)
    products = data['products']
    user_id = str(data['user_id'])
    # print("products ", products)
    # 商品订单编号
    orderNumber = "1580284" + str(int(time.time()))

    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbname)
    try:
        cursor1 = db.cursor()
        sql1 = "insert into orders(order_no, user_id) values('" + orderNumber + "',"+ user_id+")"
        cursor1.execute(sql1)
        db.commit()
        cursor2=db.cursor()
        sql2 = "select order_id from orders where order_no = '"+str(orderNumber)+"'"
        cursor2.execute(sql2)
        result = cursor2.fetchall()[0][0]
        order_id = str(result)
        cursor3 = db.cursor()
        sql3 = "insert into order_item(order_id,goods_id,goods_count) values "
        value=""
        for product in products:
            # print(product['num'])
            # print(product['productID'])
            goods_id=product['productID']
            goods_count = product['num']
            # print("goods_id ",goods_id)
            # print("goods_count ",goods_count)
            value=value+"("+str(order_id)+","+str(goods_id)+","+str(goods_count)+"),"
            # print(product)
        value = value[:-1]
        sql3 = sql3+value
        cursor3.execute(sql3)
        db.commit()
        # print("result ",result)
        code = '200'
    except:
        code = '404'
    # 关闭数据库连接
    db.close()
    return {'code': code}


if __name__ == '__main__':
    app.run(host='0.0.0.0')

    # app.run(debug=True)
