from datetime import time
from data_processor import Data_processor
from flask import Flask, url_for, request, redirect, render_template
from baha import Baha, Baha_auto_signin
from waitress import serve
from baha_auto_signin_timer import Baha_auto_signin_timer
import os
import threading
import time
import webbrowser

class Server:
    def __init__(self) -> None:
        self.app = Flask(__name__)
        self.__flask_init()
        pass

    def __flask_init(self) -> None:
        self.app.secret_key = os.urandom(64)
        self.app.jinja_env.auto_reload = True
        self.app.config['TEMPLATES_AUTO_RELOAD'] = True
        return None

    def run_server_forever(self) -> None:
        while True:
            # serve(self.app, host="0.0.0.0", port=data_processor.get_port())
            self.app.run(host='0.0.0.0', threaded=True, port=data_processor.get_port())
        return None




baha_auto_signin = Baha_auto_signin()
data_processor = Data_processor()
server = Server()
baha_auto_signin_timer = Baha_auto_signin_timer(data_processor)


@server.app.route('/', methods=['GET'])
def root():
    return redirect(url_for('status'))

@server.app.route('/setting', methods=['GET', 'POST'])
def setting():
    if request.method == 'POST':
        if "port" in request.form:
            data_processor.save_port(request.form["port"])
            # data_processor.set_restart_status(True)
            shutdown_server()
            print("port change to", data_processor.get_port())
            return redirect("http://localhost:"+str(data_processor.get_port()), code=302)
        else:
            set_setting_json(request.form)
    return render_template('setting.html')

@server.app.route('/status', methods=['GET', 'POST'])
def status():
    return render_template('status.html')

@server.app.route('/ajax/getSetting', methods=['GET'])  
def get_setting():
    return data_processor.get_setting_data()

@server.app.route('/ajax/getPort', methods=['GET'])  
def get_port():
    return str(data_processor.get_port())

@server.app.route('/ajax/getStatus', methods=['GET'])  
def get_status():
    return data_processor.get_status()

def set_setting_json(form):
    time_list = list()
    accounts_list = list()
    for i in form:
        if "time" in i:
            if form[i]!='':
                time_list.append(form[i])
        if "account" in i:
            if form[i]!='':
                tmp = {
                    "uid": form[i].split(' ')[0],
                    "passwd": form[i].split(' ')[1]
                }
                accounts_list.append(tmp)
    data_processor.save_accounts(accounts_list)
    data_processor.save_time(time_list)
    baha_auto_signin.run()
    return

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()



if __name__ == '__main__':
    if not data_processor.is_port_in_use():
        print("run server")
        threading.Thread(target=server.run_server_forever).start()
        print("open web")
        webbrowser.open('http://localhost:'+str(data_processor.get_port()) )
        baha_auto_signin.run()
        while True:
            baha_auto_signin_timer.countdown_until_time_over()
            baha_auto_signin.run()
    else: 
        print("open web")
        webbrowser.open('http://localhost:'+str(data_processor.get_port()) )