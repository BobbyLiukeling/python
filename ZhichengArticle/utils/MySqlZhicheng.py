'''
zhicheng数据库添加内容
'''
import pdb
import pymysql
import pymysql.cursors
from random import randrange
from time import ctime
import time
import hashlib
import random


class Zhicheng(object):
    def __init__(self, ):
        self.connect = pymysql.Connect(
            host = "127.0.0.1",
            db = "zhichengariticle",
            user = "root",
            passwd = "867425",
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            # use_unicode=True,
            # port=3306,
        )
        self.cursor = self.connect.cursor()

    def randtime(self,count):#生成一个从当前时间往后推三年的随机时间字符串
        dtstr = []
        for i in range(count):
            dtint = randrange(0, 90000000, 1)
            t = ctime(time.time() - dtint)  # 将生成的dtint转换成日期：日期从1970-1-1加上dtint秒数
            t = t.split(' ')
            month = str(randrange(1, 12, 1))
            t = t[-1] + '-' + month + '-' + t[-3] + ' ' + t[-2]
            dtstr.append(t)
        return dtstr

    def get_connect(self):
        connect = pymysql.Connect(
            host="loclhost",
            port=3306,
            user="root",
            passwd="867425",
            db="zhichengariticle",
            charset="utf8"
        )
        cursor = connect.cursor()
        return cursor

    def get_username(self):#获取数据库用户名
        cursor = self.get_connect()
        sql1 = "SELECT A_user from answer "
        sql2 = "SELECT user from buycar "
        sql3 = "SELECT user from question "

        cursor.execute(sql1)
        N = cursor.fetchall()
        username = []
        for i in N:
            username.append(list(i))

        cursor.execute(sql2)
        N = cursor.fetchall()
        for i in N:
            username.append(list(i))

        cursor.execute(sql3)
        N = cursor.fetchall()
        for i in N:
            username.append(list(i))

        return username

    def get_Md5(self,count): #生成加密密码
        admin = []
        for i in range(count):
            st = str(randrange(0,1000000,1))
            m = hashlib.md5()
            m.update(st.encode("utf8"))
            admin.append(m.hexdigest())
        return admin

    def get_mobile(self,count):#得到手机号码
        str = []
        for i in range(count):
            prelist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152",
                       "153",
                       "155", "156", "157", "158", "159", "186", "187", "188"]
            str.append(random.choice(prelist) + "".join(random.choice("0123456789") for _ in range(8)))
        return str

    def get_userinfo(self):#所有的信息列表
        info = []

        username = self.get_username()
        count = len(username)
        password = self.get_Md5(count)
        date_joined = self.randtime(count)
        add_time = date_joined
        city = self.city()
        citynumber = len(city)
        mobile = self.get_mobile(count)
        gender = ['男','女']

        for i in range(count):
            date = []
            date.append(password[i])
            date.append(randrange(0,1,1))#is_sign
            date.append(username[i])
            date.append(randrange(0, 1, 1))  # is_staff
            date.append(randrange(0, 1, 1))  # is_active
            date.append(date_joined[i])
            date.append(city[randrange(0,citynumber,1)])
            date.append(0)
            date.append(mobile[i])
            date.append(gender[randrange(0,2,1)])
            date.append(date_joined[i])
            info.append(date)
        return info



    def do_userinsert(self):

        #插入userinfo
        info = self.get_userinfo()
        for i in info:
            try:
                sql = "insert into users_userprofile(password,is_superuser,username,is_staff,is_active," \
                      "date_joined,city,credit,mobile,gender,add_time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                self.cursor.execute(sql, i)
            except Exception as e:
                pass

    def city(self):
        City = ['北京市', '天津市', '石家庄市', '唐山市', '秦皇岛市', '邯郸市', '邢台市', '保定市',
                '张家口', '承德市', '沧州市', '廊坊市', '衡水市', '太原市', '大同市', '阳泉市', '长治市',
                '晋城市', '朔州市', '忻州市', '吕梁市', '晋中市', '临汾市', '运城市', '呼和浩特市',
                '包头市', '乌海市', '赤峰市', '呼伦贝尔市', '兴安盟', '通辽市', '锡林郭勒盟',
                '乌兰察布盟', '伊克昭盟', '巴彦淖尔盟', '阿拉善盟', '沈阳市', '大连市', '鞍山市',
                '抚顺市', '本溪市', '丹东市', '锦州市', '营口市', '阜新市', '辽阳市', '盘锦', '铁岭市',
                '朝阳市', '葫芦岛市', '长春市', '吉林市', '四平', '辽源市', '通化市', '白山市', '松原市',
                '白城市', '延边朝鲜族自治州', '哈尔滨市', '齐齐哈尔市', '鹤岗市', '双鸭山', '鸡西市',
                '大庆市', '伊春市', '牡丹江市', '佳木斯市', '七台河市', '黑河市', '绥化市',
                '大兴安岭地区', '上海市', '南京市', '苏州市', '无锡市', '常州市', '镇江市', '南通市',
                '泰州市', '扬州市', '盐城市', '连云港市', '徐州市', '淮安市', '宿迁市', '杭州市',
                '宁波市', '温州市', '嘉兴市', '湖州市', '绍兴市', '金华市', '衢州市', '舟山市', '台州市',
                '丽水市', '合肥市', '芜湖市', '蚌埠市', '淮南市', '马鞍山市', '淮北市', '铜陵市',
                '安庆市', '黄山市', '滁州市', '阜阳市', '宿州市', '巢湖市', '六安市', '亳州市', '池州市',
                '宣城市', '福州市', '厦门市', '莆田市', '三明市', '泉州市', '漳州市', '南平市', '龙岩市',
                '宁德市', '南昌市', '景德镇市', '萍乡市', '九江市', '新余市', '鹰潭市', '赣州市',
                '吉安市', '宜春市', '抚州市', '上饶市', '济南市', '青岛市', '淄博市', '枣庄市', '东营市',
                '烟台市', '潍坊市', '济宁市', '泰安市', '威海市', '日照市', '莱芜市', '临沂市', '德州市',
                '聊城市', '滨州市', '菏泽市', '郑州市', '开封市', '洛阳市', '平顶山市', '安阳市',
                '鹤壁市', '新乡市', '焦作市', '濮阳市', '许昌市', '漯河市', '三门峡市', '南阳市',
                '商丘市', '信阳市', '周口市', '驻马店市', '焦作市', '武汉市', '黄石市', '十堰市',
                '荆州市', '宜昌市', '襄樊市', '鄂州市', '荆门市', '孝感市', '黄冈市', '咸宁市', '随州市',
                '恩施土家族苗族自治州', '仙桃市', '天门市', '潜江市', '神农架林区', '长沙市', '株洲市',
                '湘潭市', '衡阳市', '邵阳市', '岳阳市', '常德市', '张家界市', '益阳市', '郴州市',
                '永州市', '怀化市', '娄底市', '湘西土家族苗族自治州', '广州市', '深圳市', '东莞市',
                '中山市', '潮州市', '揭阳市', '云浮市', '珠海市', '汕头市', '韶关市', '佛山市', '江门市',
                '湛江市', '茂名市', '肇庆市', '惠州市', '梅州市', '汕尾市', '河源市', '阳江市', '清远市',
                '南宁市', '柳州市', '桂林市', '梧州市', '北海市', '防城港市', '钦州市', '贵港市',
                '玉林市', '百色市', '贺州市', '河池市', '来宾市', '崇左市', '海口市', '三亚市',
                '五指山市', '琼海市', '儋州市', '文昌市', '万宁市', '东方市', '澄迈县', '定安县',
                '屯昌县', '临高县', '白沙黎族自治县', '昌江黎族自治县', '乐东黎族自治县',
                '陵水黎族自治县', '保亭黎族苗族自治县', '琼中黎族苗族自治县', '重庆市', '成都市',
                '自贡市', '攀枝花市', '泸州市', '德阳市', '绵阳市', '广元市', '遂宁市', '内江市',
                '乐山市', '南充', '眉山市', '宜宾市', '广安市', '达州市', '雅安市', '巴中市', '资阳市',
                '阿坝藏族羌族自治州', '甘孜藏族自治州', '凉山彝族自治州', '贵阳市', '六盘水市', '遵义市', '安顺市',
                '铜仁地区', '毕节地区', '黔西南布依族苗族自治州', '黔东南苗族侗族自治州', '黔南布依族苗族自治州',
                '昆明市', '曲靖市', '玉溪市', '保山市', '昭通市', '丽江市', '普洱市', '临沧市',
                '德宏傣族景颇族自治州', '怒江傈僳族自治州', '迪庆藏族自治州', '大理白族自治州', '楚雄彝族自治州',
                '红河哈尼族彝族自治州', '文山壮族苗族自治州', '西双版纳傣族自治州', '拉萨市', '那曲地区', '昌都地区',
                '林芝地区', '山南地区', '日喀则地区', '阿里地区', '西安市', '铜川市', '宝鸡市', '咸阳市', '渭南市',
                '延安市', '汉中市', '榆林市', '安康市', '商洛市', '兰州市', '嘉峪关市', '金昌市', '白银市', '天水市',
                '武威市', '酒泉市', '张掖市', '庆阳市', '平凉市', '定西市', '陇南市', '临夏回族自治州',
                '甘南藏族自治州', '西宁市', '海东地区', '海北藏族自治州', '海南藏族自治州', '黄南藏族自治州',
                '果洛藏族自治州', '玉树藏族自治州', '海西蒙古族藏族自治州', '银川市', '石嘴山市', '吴忠市',
                '固原市', '中卫市', '乌鲁木齐市', '克拉玛依市', '吐鲁番地区', '哈密地区', '和田地区', '阿克苏地区',
                '喀什地区', '克孜勒苏柯尔克孜自治州', '巴音郭楞蒙古自治州', '昌吉回族自治州', '博尔塔拉蒙古自治州',
                '石河子', '阿拉尔', '图木舒克', '五家渠', '伊犁哈萨克自治州', '台北市', '新北市', '桃园市', '台中市',
                '台南市', '高雄市', '澳门', '香港']
        len(City)
        #len = 368
        return City

    def insert_article(self):
        cur = self.get_connect()
        sql = "SELECT * from buycar "
        cur.execute(sql)
        N = cur.fetchall()
        article = []
        for i in N:
            article.append(list(i))

        count = len(article)
        add_time = self.randtime(count)
        # pdb.set_trace()
        update_time = add_time
        city = self.city()
        citynumber = len(city)
        Article = []
        for k in range(count):
            A = article[k]
            SQL = "select id from users_userprofile where username = '%s'" % A[1]
            user_id = 0
            try:
                self.cursor.execute(SQL)
                s = self.cursor.fetchall()
                for q in s:
                    user_id = q
            except Exception as e:
                print(e)
                user_id = 0
                pass
            date = []
            date.append(city[randrange(0, citynumber, 1)])
            date.append(A[2])#title
            date.append(A[3])  #content
            date.append(randrange(0,1000,1))  #click_number
            date.append(randrange(0,1000,1))  #fav_number
            date.append(add_time[k])  #add_time
            date.append(update_time[k])  #update_time
            date.append(randrange(0, 1, 1))  #draft
            date.append(A[-2])  #label
            # pdb.set_trace()
            date.append(int(user_id['id']))  #user_id
            Article.append(date)
        for i in Article:
            try:
                sql = "insert into articles_article(city,title,content,click_nums,fav_nums," \
                      "add_time,update_time,draft,lable,user_id) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                self.cursor.execute(sql, i)
            except Exception as e:
                print(e)
                pass

    def insert_question(self):
        cur = self.get_connect()
        sql = "SELECT * from question "
        cur.execute(sql)
        N = cur.fetchall()
        question = []
        for i in N:
            question.append(list(i))

        count = len(question)
        add_time = self.randtime(count)
        # pdb.set_trace()
        update_time = add_time
        city = self.city()
        citynumber = len(city)
        Question = []
        for k in range(count):
            A = question[k]
            SQL = "select id from users_userprofile where username = '%s'" % A[5]

            user_id = 0
            try:
                self.cursor.execute(SQL)
                s = self.cursor.fetchall()
                for q in s:
                    user_id = q
            except Exception as e:
                print(e)
                user_id = 0
                pass
            date = []
            date.append(city[randrange(0, citynumber, 1)])
            date.append(A[3])  # title
            date.append(randrange(0, 1000, 1))  # click_number
            date.append(randrange(0, 1000, 1))  # fav_number
            date.append(add_time[k])  # add_time
            date.append(randrange(0, 1, 1))  # draft
            date.append(A[1])  # label
            # pdb.set_trace()
            date.append(int(user_id['id']))  # user_id
            date.append(A[-1])  # content
            Question.append(date)
        for i in Question:
            try:
                sql = "insert into questions_question(city,title,click_nums,fav_nums," \
                      "add_time,draft,label,user_id,content) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                self.cursor.execute(sql, i)
            except Exception as e:
                print(e)
                pass




    def close(self):
        self.connect.commit()  # 不提交到不了数据库中
        self.connect.close()

if __name__=='__main__':
    U = Zhicheng()
    # U.do_userinsert()
    U.insert_article()
    # U.insert_question()
    U.close()






