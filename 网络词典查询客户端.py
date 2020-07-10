'''
dict 客户端
发起请求
获取结果为客户展示
'''


from socket import *
import sys

#服务器地址
ADDR = ('127.0.0.1',8888)

#查历史记录
def do_history(sockfd,name):
    msg = 'H %s'%name
    sockfd.send(msg.encode())
    #不能确定实际接收次数
    while True:
        data = sockfd.recv(2048).decode()
        if data == '##':
            break
        print(data)


#查单词
def do_query(sockfd,name):
    while True:
        word = input('请输入单词:')
        if word == '##':
            break
        msg = 'Q %s %s'%(name,word)
        sockfd.send(msg.encode())
        #如果查到单词给我返回解释，没查到给我返回没有查到，无论什么结果我直接打印
        data = sockfd.recv(2048)
        print(data.decode())


#封装二级界面 name的身份登录
def login(sockfd,name):
    #进入登录界面
    while True:
        print('''
         -----------webcome-----------
         1.查单词    2.历史记录    3.注销
         -----------------------------
         ''')
        cmd = input("请输入选项：")
        if cmd == '1':
            do_query(sockfd,name)
        elif cmd == '2':
            do_history(sockfd,name)
        elif cmd == '3':
            return
        else:
            print('请输入正确选项(1,2,3)')

#注册
def do_register(sockfd):
    while True:
        name = input('User:')
        passwd = input('Password:')
        if (' ' in name) or (' ' in passwd):
            print('用户名密码不能有空格')
            continue
        msg = 'R %s %s'%(name,passwd)
        sockfd.send(msg.encode())#发送请求
        #等待结果
        data = sockfd.recv(128).decode()
        if data == 'YES':
            print('注册成功')
            break
        else:
            print('注册失败')
        return

#登录
def do_login(sockfd):
    name = input('user:')
    passwd = input('password:')

    msg = 'L %s %s'%(name,passwd)
    sockfd.send(msg.encode())
    #等待结果
    data = sockfd.recv(128).decode()
    if data == 'YES':
        print('登录成功')
        login(sockfd,name)
    else:
        print('请输入正确的账号或密码')
    return


#客户端网络搭建
def main():
    #创建套接字
    sockfd = socket()
    sockfd.connect(ADDR)
    #进入登录界面
    while True:
        print('''
        ---------webcome---------
        1.注册    2.登录    3.退出
        -------------------------
        ''')
        cmd = input("请输入选项：")
        if cmd == '1':
            do_register(sockfd)
        elif cmd == '2':
            do_login(sockfd)
        elif cmd == '3':
            sockfd.send(b'E')
            sys.exit('谢谢使用')
        else:
            print('请输入正确选项(1,2,3)')


if __name__ == '__main__':
    main()