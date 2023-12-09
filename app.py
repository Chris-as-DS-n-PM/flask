from flask import Flask, request, Response

app = Flask(__name__)


@app.route('/_about')
def about():
    return Response("<?xml version=\"1.0\" encoding=\"UTF-8\" ?><html>about</html>", content_type='text/xml')


@app.route('/')
def index():
    return Response("<title>Login to SHR-H1</title>", content_type='text/xml')


@app.route('/cgi-bin/systemutil.cgi', methods=['POST'])
def system_util():
    params = request.form
    code = "2" if params.get("user") == "admin" and params.get("password") == "admin" else "0"
    response_content = "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n" + \
                       "<xml>\n" + \
                       "<Login>{}</Login>\n".format(code) + \
                       "</xml>"
    return Response(response_content, content_type='text/xml')


@app.route('/cgi-bin/modem.cgi', methods=['GET'])
def modem_cgi():
    command = request.args.get("Command")
    if command == "getAntenna":
        response_content = "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n" + \
                           "<xml>\n" + \
                           "<antenna_value>2</antenna_value>\n" + \
                           "</xml>\n"
    elif command == "getModemStatus":
        response_content = "<xml>\n" + \
                           "<Model>NTMORE NTLM-500</Model>\n" + \
                           "<FwVer>NTM_M500_R01.1-27</FwVer>\n" + \
                           "<ESN></ESN>\n" + \
                           "<IMEI>357936050259427</IMEI>\n" + \
                           "<MEID></MEID>\n" + \
                           "<IMSI>250207491225562</IMSI>\n" + \
                           "<MSISDN></MSISDN>\n" + \
                           "<CmState>10</CmState>\n" + \
                           "<UiccType>1</UiccType>\n" + \
                           "<Uicc_status>2</Uicc_status>\n" + \
                           "<Uicc_Pin_status>3</Uicc_Pin_status>\n" + \
                           "<Uicc_Pin_num_pin>3</Uicc_Pin_num_pin>\n" + \
                           "<Uicc_Pin_num_puk>10</Uicc_Pin_num_puk>\n" + \
                           "<Rf_isUpdate>1</Rf_isUpdate>\n" + \
                           "<RAT>LTE 31</RAT>\n" + \
                           "<rssi>-85</rssi>\n" + \
                           "<rscp>255</rscp>\n" + \
                           "<rsrp>-108</rsrp>\n" + \
                           "<mcc>250</mcc>\n" + \
                           "<mnc>20</mnc>\n" + \
                           "<arfcn>9897</arfcn>\n" + \
                           "<cellid>146</cellid>\n" + \
                           "<sinr>  5.0</sinr>\n" + \
                           "<ecno>255</ecno>\n" + \
                           "<rsrq>-15.0</rsrq>\n" + \
                           "<earfcn_dl>65535</earfcn_dl>\n" + \
                           "<earfcn_ul>65535</earfcn_ul>\n" + \
                           "<ci></ci>\n" + \
                           "<pci>65535</pci>\n" + \
                           "<tac>65535</tac>\n" + \
                           "<drx>65535</drx>\n" + \
                           "<tmsi></tmsi>\n" + \
                           "<srv_status>255</srv_status>\n" + \
                           "<rrc_state>255</rrc_state>\n" + \
                           "<emm_state>255</emm_state>\n" + \
                           "<emm_substate>255</emm_substate>\n" + \
                           "<bandwidth>255</bandwidth>\n" + \
                           "<RegiStatus>1</RegiStatus>\n" + \
                           "<IpAddr>10.232.192.164</IpAddr>\n" + \
                           "<netItf>eth0</netItf>\n" + \
                           "<emm_status_str></emm_status_str>\n" + \
                           "<emm_cause_str></emm_cause_str>\n" + \
                           "<esm_cause_str></esm_cause_str>\n" + \
                           "<psc>65535</psc>\n" + \
                           "<rrc_state_str></rrc_state_str>\n" + \
                           "<reject_cause>255</reject_cause>\n" + \
                           "<service_domain>255</service_domain>\n" + \
                           "</xml>\n"
    else:
        return "Invalid command", 400

    return Response(response_content, content_type='text/xml')
