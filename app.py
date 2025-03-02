from flask import Flask, request, Response
import random
import time
import threading

app = Flask(__name__)

# Глобальная переменная для хранения состояния
state = {
    'reboot_in_progress': False
}

# Создаем объект блокировки для обеспечения потокобезопасности
lock = threading.Lock()

@app.route('/_about')
def about():
    return Response("<?xml version=\"1.0\" encoding=\"UTF-8\" ?><html>about</html>", content_type='text/xml')


@app.route('/')
def index():
    return Response("<title>Login to SHR-H1</title>", content_type='text/xml')


@app.route('/cgi-bin/systemutil.cgi', methods=['POST'])
def system_util():
    params = request.form
    command = params.get("Command")
    response_content = ""
    if command == "Login":
        code = "2" if params.get("user") == "admin" and params.get("password") == "admin" else "0"
        response_content = "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n" + \
                           "<xml>\n" + \
                           "<Login>{}</Login>\n".format(code) + \
                           "</xml>"
    elif command == "RebootSystem":
        with lock:
            state['reboot_in_progress'] = True  # Устанавливаем флаг

    return Response(response_content, content_type='text/xml')

def create_random_digits(length):
    """Generate a string of random digits of a given length."""
    return ''.join(random.choices('0123456789', k=length))


@app.route('/cgi-bin/modem.cgi', methods=['GET'])
def modem_cgi():
    with lock:
        # Проверяем, было ли завершение перезагрузки
        if state['reboot_in_progress']:
            time.sleep(10)
            state['reboot_in_progress'] = False  # Сброс флага после использования

    command = request.args.get("Command")
    if command == "getAntenna":
        response_content = "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n" + \
                           "<xml>\n" + \
                           "<antenna_value>2</antenna_value>\n" + \
                           "</xml>\n"

    elif command == "getModemStatus":
        modem_status = [
            "<Model>NTMORE NTLM-500</Model>",
            "<FwVer>NTM_M500_R01.1-27</FwVer>",
            "<ESN>{}</ESN>".format(create_random_digits(16)),  # Example ESN
            "<IMEI>357936050259427</IMEI>"
            "<MEID>{}</MEID>".format(create_random_digits(14)),  # Example MEID
            "<IMSI>250207491225562</IMSI>"
            "<MSISDN>{}</MSISDN>".format(create_random_digits(10)),  # Example 10-digit MSISDN
            "<CmState>10</CmState>",
            "<UiccType>1</UiccType>",
            "<Uicc_status>2</Uicc_status>",
            "<Uicc_Pin_status>3</Uicc_Pin_status>",
            "<Uicc_Pin_num_pin>3</Uicc_Pin_num_pin>",
            "<Uicc_Pin_num_puk>10</Uicc_Pin_num_puk>",
            "<Rf_isUpdate>1</Rf_isUpdate>",
            "<RAT>LTE 31</RAT>",
            "<rssi>{}</rssi>".format(random.randint(-120, -50)),  # Random RSSI value
            "<rscp>{}</rscp>".format(random.randint(0, 255)),      # Random RSCP value
            "<rsrp>{}</rsrp>".format(random.randint(-120, -60)),   # Random RSRP value
            "<mcc>{}</mcc>".format(random.randint(250, 999)),       # Random MCC
            "<mnc>{}</mnc>".format(random.randint(0, 99)),          # Random MNC
            "<arfcn>{}</arfcn>".format(random.randint(9600, 9750)), # Random ARFCN
            "<cellid>{}</cellid>".format(random.randint(1, 3000)),  # Random Cell ID
            "<sinr>{:.1f}</sinr>".format(random.uniform(0, 30)),    # Random SINR
            "<ecno>{}</ecno>".format(random.randint(0, 255)),        # Random ECNO
            "<rsrq>{:.1f}</rsrq>".format(random.uniform(-20, 0)),   # Random RSRQ
            "<earfcn_dl>{}</earfcn_dl>".format(random.randint(0, 65535)),  # Random DL EARFCN
            "<earfcn_ul>{}</earfcn_ul>".format(random.randint(0, 65535)),  # Random UL EARFCN
            "<ci></ci>",
            "<pci>{}</pci>".format(random.randint(0, 255)),          # Random PCI
            "<tac>{}</tac>".format(random.randint(0, 255)),          # Random TAC
            "<drx>{}</drx>".format(random.randint(0, 255)),          # Random DRX
            "<tmsi></tmsi>",
            "<srv_status>{}</srv_status>".format(random.randint(0, 255)),  # Random service status
            "<rrc_state>{}</rrc_state>".format(random.randint(0, 255)),    # Random RRC state
            "<emm_state>{}</emm_state>".format(random.randint(0, 255)),    # Random EMM state
            "<emm_substate>{}</emm_substate>".format(random.randint(0, 255)), # Random EMM substate
            "<bandwidth>{}</bandwidth>".format(random.randint(0, 255)),    # Random bandwidth
            "<RegiStatus>1</RegiStatus>",
            "<IpAddr>10.232.192.164</IpAddr>",
            "<netItf>eth0</netItf>",
            "<emm_status_str></emm_status_str>",
            "<emm_cause_str></emm_cause_str>",
            "<esm_cause_str></esm_cause_str>",
            "<psc>{}</psc>".format(random.randint(55535, 65535)),
            "<rrc_state_str></rrc_state_str>",
            "<reject_cause>255</reject_cause>".format(random.randint(0, 255)),
            "<service_domain>255</service_domain>".format(random.randint(0, 255)),
            ]
        response_content =  "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n<xml>\n" + "\n".join(modem_status) + "\n</xml>\n"

    else:
        return "Invalid command", 400

    return Response(response_content, content_type='text/xml')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

# if __name__ == '__main__':
#     app.run(debug=True)