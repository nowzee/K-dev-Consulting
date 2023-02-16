import ftplib
from ftplib import FTP

host = '127.0.0.1'
user = input('enter a username : ')
passwd = input('enter a password : ')

with FTP(host) as ftp:
    try:
        ftp.login(user=user, passwd=passwd)
    except ftplib.error_perm:
        print("login incorrect")
        exit()

    while True:
        command = input('enter command : ')

        if command == 'push_all':

            ftp.cwd('templates')
            with open('templates/index.html', 'rb') as f:
                ftp.storbinary('STOR index.html', f)
                f.close()
            ftp.cwd('../static')
            with open('static/css.css', 'rb') as f:
                ftp.storbinary('STOR css.css', f)
                ftp.cwd('../')
                f.close()
            print('send file success')

        elif command == 'exit':
            print('quit')
            ftp.quit()
            exit()

        elif command == 'push_templates':
            ftp.cwd('templates')
            with open('templates/index.html', 'rb') as f:
                ftp.storbinary('STOR index.html', f)
                ftp.cwd('../')
                f.close()
                print('send file success in templates only')

        elif command == "push_static":
            with open('static/css.css', 'rb') as f:
                ftp.storbinary('STOR css.css', f)
                ftp.cwd('../')
                f.close()
            print('send file success in static only')

        else:
            print('push : send all file to webserver\n'
                  'exit : quit ftp server\n'
                  'push_templates : only push in templates\n'
                  'push_static : only push in static')
