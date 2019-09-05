
import requests_html as requests
from lxml import etree
import json
import time
from PIL import Image
session = requests.HTMLSession()
header = {
    'Accept':'image/webp,image/apng,image/*,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Host': 'zhjw.scu.edu.cn',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'Referer': '',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, '
              'like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3676.400 QQBrowser/10.4.3505.400'
}
headerspost = {
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; LCTE; rv:11.0) like Gecko',
    'Content-Type': 'application/json',
    'Accept': '*/*',
    'Referer': 'http://zhjw.scu.edu.cn/student/teachingEvaluation/teachingEvaluation/evaluationPage',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN',
    'Host':'zhjw.scu.edu.cn',
    'Content-Type':'application/x-www-form-urlencoded',
    'charset':'UTF-8'
}
formData = {'j_username': '0', 'j_password': '0', 'j_captcha': 'error'}
def login():
    print("URP评教软件Ver1.1,,by MIA")
    #cookies = session.cookies.get_dict()
    session.get('http://zhjw.scu.edu.cn/img/captcha.jpg')
    #cookies['safedog-flow-item'] = ''
    #cookies['selectionBar'] = '1293218'
    header['Referer'] = 'http://zhjw.scu.edu.cn/img/captcha.jpg'
    captcha = session.get('http://zhjw.scu.edu.cn/img/captcha.jpg')
    formData['j_username'] = input("请输入账号：")
    formData['j_password'] = input("请输入密码：")
    with open('test.jpg', 'wb') as fd:
        fd.write(captcha.content)

    captcha_image = Image.open('test.jpg')
    captcha_image.show()
    formData['j_captcha'] = input("请输入验证码：")
    #formData = {'j_username': j_username, 'j_password': j_password, 'j_captcha1': 'error'}
    #header['Cookie'] = requests.cookies.RequestsCookieJar()
    header['Referer'] = 'http://zhjw.scu.edu.cn/j_spring_security_check'
    response = session.post(url='http://zhjw.scu.edu.cn/j_spring_security_check',
                            data=formData)
    serachUrl='http://zhjw.scu.edu.cn/student/teachingEvaluation/teachingEvaluation/search'
    header['Referer'] = serachUrl
    getMsg = session.get(url=serachUrl, allow_redirects=False)
    code = getMsg.status_code
    if code < 300:
        print("登陆成功！")
        teacherMsg = json.loads(getMsg.text)
        evaluate(teacherMsg)
    else:
        print("密码错误或发生未知错误！五秒后自动退出")
        time.sleep(5)
        exit(0)


def evaluate(teacherMsg):
    for eachteacherMsg in teacherMsg["data"]:
        if eachteacherMsg["evaluatedPeople"] == "屈立茄":
            print("恭喜你触发彩蛋：屈老狗请自行评价！")
            continue
        #sessiontest = requests.session()
        #response = session.post(url='http://zhjw.scu.edu.cn/j_spring_security_check', data=formData)
        msgdict={}
        msgdict["evaluatedPeople"]=eachteacherMsg["evaluatedPeople"]
        msgdict["evaluatedPeopleNumber"]=eachteacherMsg["id"]["evaluatedPeople"]
        msgdict["questionnaireCode"] = eachteacherMsg["id"]["questionnaireCoding"]
        msgdict["questionnaireName"] = eachteacherMsg["questionnaire"]["questionnaireName"]
        msgdict["evaluationContentNumber"]=eachteacherMsg["id"]["evaluationContentNumber"]
        msgdict["evaluationContentContent"] = ""
        evaluateUrl="http://zhjw.scu.edu.cn/student/teachingEvaluation/teachingEvaluation/evaluationPage"
        response = session.post(url=evaluateUrl, data=msgdict)
        evaluateMsg={}
        print("正在评教课程:"+eachteacherMsg["evaluationContent"]+msgdict["questionnaireName"])
        evaluateMsg["tokenValue"] = str((response.html.xpath('//*[@id="tokenValue"]/@value'))[0])
        evaluateMsg["questionnaireCode"]=msgdict["questionnaireCode"]
        evaluateMsg["evaluationContentNumber"] = msgdict["evaluationContentNumber"]
        evaluateMsg["evaluatedPeopleNumber"] = msgdict["evaluatedPeopleNumber"]
        evaluateMsg["count"] = 0
        strchoose="学生评教（课堂教学）"

        labelnameMsg=etree.HTML(response.text).xpath('//*[@id="page-content-template"]/div/div/div[1]/form/div/table/tbody/tr')
        count = 0
        for eachlabel in labelnameMsg:
            try:
                label=eachlabel.xpath('//div[1]/label/input')[count].get('name')
                evaluateMsg[str(label)]="10_1"
            except IndexError:
                continue
            count+=1

        '''
        if msgdict["questionnaireName"].encode('utf-8') == strchoose.encode('utf-8') :
            for i in range(7):
                evaluateMsg["00000000"+str(i+36)]= "10_1"
        else:
                for i in range(6):
                    evaluateMsg["00000000" + str(i+28)] = "10_1"
        '''
        evaluateMsg["zgpj"]= "非常棒的老师"
       # print(evaluateMsg["questionnaireCode"], evaluateMsg["tokenValue"], evaluateMsg["zgpj"],msgdict["evaluatedPeople"],msgdict["questionnaireName"])
        postUrl="http://zhjw.scu.edu.cn/student/teachingEvaluation/teachingEvaluation/evaluation"
        rq = session.post(url=postUrl,data=evaluateMsg,headers=headerspost)
        code = rq.status_code
        if code<300:
            print("评教成功！")
        else:
            print("出现错误，本课程已评教！")
            continue
        #session.get(url="http://zhjw.scu.edu.cn/logout")
        #session.get(url="http://zhjw.scu.edu.cn/enterOut")
        time.sleep(122)


login()
print("评教完毕！十五秒钟后自动退出")
time.sleep(15)

'''
evaluatedPeopleNumber	80132145
questionnaireCode	0000000075
questionnaireName	学生评教（课堂教学）
evaluationContentNumber	107117000
evaluationContentContent	
http://zhjw.scu.edu.cn/student/teachingEvaluation/teachingEvaluation/evaluationPage
//*[@id="page-content-template"]/div/div/div[1]/form/input[1]
tokenValue	3a6bcf51f4b1f925b9f84faa03cd113d
questionnaireCode	0000000075
evaluationContentNumber	107117000
evaluatedPeopleNumber	80132145
0000000036	10_1
0000000037	10_1
0000000038	10_1
0000000039	10_1
0000000040	10_1
0000000041	10_1
0000000042	10_1
zgpj	非常好的老师！
http://zhjw.scu.edu.cn/student/teachingEvaluation/teachingEvaluation/evaluation
'''