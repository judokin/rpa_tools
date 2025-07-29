def error_msg():
    import requests
    import json
    import socket

    # 获取当前计算机名称
    computer_name = socket.gethostname()

    print(f"当前计算机名称是: {computer_name}")
    # 替换为你的飞书 Webhook URL
    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/c6418617-4971-41b2-a00f-60b27e72007f"

    # 发送的消息内容
    message = {
        "msg_type": "text",
        "content": {
            "text": f"{computer_name}电脑报错了，请注意查看情况"
        }
    }

    # 发送请求
    response = requests.post(webhook_url, headers={"Content-Type": "application/json"}, data=json.dumps(message))

    # 打印结果
    if response.status_code == 200:
        print("消息发送成功")
    else:
        print(f"消息发送失败: {response.text}")
def get_reviews_by_url(sku=''):
    import requests

    cookies = {
        'CSNUtId': '89b316d1-cb83-48f9-a3a0-993c5c25092e',
        'i18nPrefs': 'lang%3Den-US',
        'ExCSNUtId': '89b316d1-cb83-48f9-a3a0-993c5c25092e',
        '_pxvid': '2f37446f-fa20-11ef-b233-483ed9754125',
        '__pxvid': '2fc9176f-fa20-11ef-8c6f-0242ac120002',
        'salsify_session_id': 'b1e1d55f-19be-48fc-85bc-c62b20aa0a35',
        '__ssid': 'd5fb35a47d5613d1c8309ffa5b2af9e',
        'cjConsent': 'MHxOfDB8Tnww',
        'cjUser': '0584478d-0330-42a6-a747-c755d01e97c5',
        '_axwrt': '231dbf38-99ac-43c0-b613-bb18c2bb4ec6',
        '__podscribe_wayfair_referrer': '_',
        '__podscribe_wayfair_landing_url': 'https://www.wayfair.com/rugs/pdp/bungalow-rose-oriental-boho-vintage-print-machine-washable-area-rug-maroon-red-low-pile-high-with-non-slip-backing-for-high-traffic-area-w111359465.html?piid=242722570',
        '__podscribe_did': 'pscrb_3324b67a-4673-4cca-c172-b5d5c6058533',
        'rskxRunCookie': '0',
        'rCookie': 'z3siebrhcgrbb06zee4wysm7wlknml',
        '_tt_enable_cookie': '1',
        '_ttp': '01JNMD0R02FPHJG14NWP9N8WAY_.tt.1',
        '__attentive_id': 'f1f779439ec14f528531d03c489026c0',
        '__attentive_cco': '1741220241790',
        'axwrt': '231dbf38-99ac-43c0-b613-bb18c2bb4ec6',
        'attntv_mstore_email': 'a249022968@gmail.com:0',
        'CSN_RT': '9566856C04E58E1EA219C707E4BBB5BEC061732B5EDA406D9F4BE3B7FD464614',
        'CSNID': '9C769B99-F64C-4B2B-92BB-BEA485225AA3',
        'WFCS': 'CS3',
        '__attentive_client_user_id': '0e39ce9f145fe192ddf13172fc8758d4461db31ae5ed2a9c1b0f39f5cf3ec6a1',
        '_alby_user': '76daa402-04af-422f-bc78-ad04e032610a',
        '_ga_Q0HJWP456J': 'deleted',
        '_ga_0GV7WXFNMT': 'deleted',
        '_uetvid': '56c2f9b0fa2011efb07fd7c1d99fb8a7',
        'ndp_session_id': 'f75cbd2e-2780-4e5a-9c5a-19abf454819a',
        'ibb': '1',
        'postalCode': '67346',
        'SFSID': '6384f0bbb3246c8a987824d6b0af8c7f',
        'serverUAInfo': '%7B%22browser%22%3A%22Google%20Chrome%22%2C%22browserVersion%22%3A136%2C%22OS%22%3A%22Windows%22%2C%22OSVersion%22%3A%22%22%2C%22isMobile%22%3Afalse%2C%22isTablet%22%3Afalse%2C%22isTouch%22%3Afalse%7D',
        'pxcts': '6197c0c5-3065-11f0-beb4-c7213f7e90cd',
        'IR_gbd': 'wayfair.com',
        '_gid': 'GA1.2.27009705.1747614611',
        '_ga_0GV7WXFNMT': 'deleted',
        '_ga_Q0HJWP456J': 'deleted',
        'canary': '0',
        '_gcl_au': '1.1.417332783.1741220240.1295446020.1748308354.1748308429',
        '_pxhd': 'Nv3Yuo7nF6tEUtjkAO7AxcB8YwKbvBrDOv2z2xBrCmCyzhEy1rS5mlavQkhr7htQjRfo5CQb6fH1kIeTpr6sbg==:nFAF2M4p0JGgv6g2EWKSq6qSp8inUBtURHAKByKAner2MHjUecBmhzQ/-P2QAOe/wea7IEitTn1JnjGmE4PZJtiusAMbqaYPTu1fbyWperA=',
        'CSN_CSRF': '66c5ff8ebc99cf28d65700146c1eb0ad15ae16dfe94265aedf2e4bc0a322f93b',
        '__attentive_dv': '1',
        'vid': '56d9465d-0629-4e53-8489-443bb705e641',
        'WFDC': 'DSM',
        'CSN_CT': 'eyJhbGciOiJSUzI1NiIsImtpZCI6InBlRG5BMWVVVGRVQU00YVdjU3FnZm40ZEJhbFZCYnJ4R2ZEU0ZQYXVQbG8iLCJ4NXQiOiJJMkJNSDFJREVoUUVmamNtdDZrcU02d3BiME0iLCJ0eXAiOiJKV1QiLCJqa3UiOiJodHRwczovL3Nzby5hdXRoLndheWZhaXIuY29tLy53ZWxsLWtub3duL29wZW5pZC1jb25maWd1cmF0aW9uL2p3a3MifQ.eyJuYmYiOjE3NDg0MTQ0NjUsImV4cCI6MTc0ODQyODg2NiwiaWF0IjoxNzQ4NDE0NDY2LCJpc3MiOiJodHRwczovL3Nzby5hdXRoLndheWZhaXIuY29tLyIsImF1ZCI6ImF1dGhfaWRlbnRpdHkiLCJjbGllbnRfaWQiOiJ5NnZVV0dUd2dFVlA0VEFZbXZuTGxBIiwiY3VpZCI6IjYxNzQxMTc5MTMiLCJzdWIiOiIzMDk0MjQxMTAiLCJ2ZXJzaW9uIjoiMi4wIiwicGx0Ijoid2ViIiwib3JpZ2luYWxfaWF0IjoiMTc0NDE2MzIwNyIsInJvbGUiOiJzZjpjdXN0b21lciIsImp0aSI6IjY0MEIyOTk1N0U1QUEwMENGNUQ5MzA0MDREQzdFQUNBIiwic2NvcGUiOiJvcGVuaWQgb2ZmbGluZV9hY2Nlc3Mgc2Y6cmVjb2duaXplZCBzZjp0cnVzdGVkIiwiYW1yIjpbImNyZWF0ZV91c2VyIiwicmVmcmVzaCJdfQ.TNwu4B8iFUzGatD-DxuPWU8HC7dqOlZEyJvAqjrFWDmKVYrKFPZm9dzzyFcVFyun9rNEmBl7XgRrwR45gIVzdkr2TI_OktsMuD-r_TuzUxWr4rdaITaoCJdivA2EuZwsob2Od-evfZ6apCIXB-pmH6iWEIxr3QNbf5OqXMCoJnEVeU8cFxBKUwodX72lRX1dRWxZ40bvp48bLf_mCipPZRDI_k6Hu995r2CGXMF2U9Ud6UwrfB_648451UZwdHICvUtt-0fC3Rn12ZMFKxEkXuUAwy8K4wH3H2VD6J5D5W5VfpUh0j_XxNh5hBmOTQsoNp4JOS57gCsrPk8cbH0LRvffivDn8U5OurYUYjoipH6n5-rw8W-mGNwAd3wsq9aObIYo_AoANPCS4TE88pXiTyun7CtdlMSicUjV25ye5eZSBeSjnN7WvHvXvFuH2SKMKe1Rt5CBV25IMNGI71nkOhterKyrPgQeDYDg-w--VHKvdja3xG7clfTl7HvW-r8o1VSAnRWvRyfCP5IJyBOD3OMYH3falk7o18YNZUnLVTfFkqPOdViOZFYds7bDXJS2cgDL3CPlZ9W1nJgnDo_PK-E3DkBXnPPO_IBgej5G9eMEEt49WhrEYhEOUFIu1GSXqgocwXAzVZRyi60Ds1dv6VTKZBj1zVb49xBsgfR1neA',
        '__attentive_session_id': 'faa36bb136e343c099d0a7914b8c141c',
        '__attentive_ss_referrer': 'ORGANIC',
        '_px3': 'd5ec0bfabd958951a546d032b45a5586114f05f440151be0d5ed8aedb96e62ac:hGnmqBX7H4yvqbWapdmN3bAHz6KhqkxrtsOkI+Drqy+HpeEKaWF028+G5k6do+Vgt77cUn6Pn93fmAgig/iTBg==:1000:I9CxbeOJUQzM11XcAln1JFLbT1jOnO7+AVIHzwneKOPLWzv0J+ijWInZKzFJnQ70c9zKZFnK4dBPBBpgH38HlSbbjBbWwje/v0XDyYcFsAPQRncH8U3qtZITor7/O7nHktdFOM3Qqwar6Csi1becFvp8IH4g8rXoQqcaydOv8NXpg11HSomcRM/uiljfygc/GJyEYYulOhI7Or45ytL4mUCGTQHJrEvALCzE6aJ8CCA=',
        'otx': 'IuTn+7zQTna6mdd5KRGoVw==',
        '__wid': '503578700',
        'ax_visitor': '%7B%22firstVisitTs%22%3A1741220225682%2C%22lastVisitTs%22%3A1748403702408%2C%22currentVisitStartTs%22%3A1748414464937%2C%22ts%22%3A1748421674962%2C%22visitCount%22%3A103%7D',
        '_rdt_uuid': '1741220227124.e1710325-d83d-4119-a820-5cc7a3c12483',
        '_rdt_em': '0e39ce9f145fe192ddf13172fc8758d4461db31ae5ed2a9c1b0f39f5cf3ec6a1:0e39ce9f145fe192ddf13172fc8758d4461db31ae5ed2a9c1b0f39f5cf3ec6a1',
        '_uetsid': '0671d4c0344e11f0a1d469c877b3b8d7',
        'forterToken': '5349ac441e664549a50d947c6faa35fd_1748421664547_5706_UDF43-mnf-a4_25ck_REluqn+URlE%3D-1962-v2',
        'forterToken': '5349ac441e664549a50d947c6faa35fd_1748421664547_5706_UDF43-mnf-a4_25ck_REluqn+URlE%3D-1962-v2',
        'IR_12051': '1748421680314%7C0%7C1748421680314%7C%7C',
        'IR_PI': '3c3e4f6a-14e8-11f0-8c2a-a5fe5042a2dc%7C1748421680314',
        'lastRskxRun': '1748421681343',
        '_ga_0GV7WXFNMT': 'GS2.1.s1748420911$o184$g1$t1748421683$j15$l0$h0',
        'CSNPersist': 'page_of_visit%3D2013',
        '_attn_': 'eyJ1Ijoie1wiY29cIjoxNzQxMjIwMjQxNzg5LFwidW9cIjoxNzQxMjIwMjQxNzg5LFwibWFcIjoyMTkwMCxcImluXCI6ZmFsc2UsXCJ2YWxcIjpcImYxZjc3OTQzOWVjMTRmNTI4NTMxZDAzYzQ4OTAyNmMwXCJ9Iiwic2VzIjoie1widmFsXCI6XCJmYWEzNmJiMTM2ZTM0M2MwOTlkMGE3OTE0YjhjMTQxY1wiLFwidW9cIjoxNzQ4NDIxNjg1NTcxLFwiY29cIjoxNzQ4NDIxNjg1NTcxLFwibWFcIjowLjAyMDgzMzMzMzMzMzMzMzMzMn0ifQ==',
        '_gat_gtag_UA_2081664_4': '1',
        '_ga_Q0HJWP456J': 'GS2.1.s1748420911$o179$g1$t1748421686$j12$l0$h0',
        '_ga': 'GA1.1.1847679220.1741220240',
        'ttcsid': '1748420908738::XgSOmwkwvYLac8ld8Fm0.159.1748421688634',
        'ttcsid_C7KTM4O68TKN71DEGAK0': '1748420908735::VIr-v6vX2gmMibnd9CoB.157.1748421688866',
        '__attentive_pv': '3',
    }

    headers = {
        'accept': 'application/json',
        'accept-language': 'zh-CN,zh;q=0.9',
        'apollographql-client-name': '@wayfair/sf-ui-product-details',
        'apollographql-client-version': '44974d056c3ad3dc287fa918823d74280d7ebc9f',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://www.wayfair.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.wayfair.com/rugs/pdp/janousek-oriental-gray-area-rug-w005932099.html?piid=718030887&auctionId=62f82b49-474f-4b14-be2d-14d121ba38fb&adTypeId=1',
        'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'use-web-hash': 'true',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        'x-parent-txid': '0RgVOI7ZSIW3DL6K0pUzMw==',
        # 'cookie': 'CSNUtId=89b316d1-cb83-48f9-a3a0-993c5c25092e; i18nPrefs=lang%3Den-US; ExCSNUtId=89b316d1-cb83-48f9-a3a0-993c5c25092e; _pxvid=2f37446f-fa20-11ef-b233-483ed9754125; __pxvid=2fc9176f-fa20-11ef-8c6f-0242ac120002; salsify_session_id=b1e1d55f-19be-48fc-85bc-c62b20aa0a35; __ssid=d5fb35a47d5613d1c8309ffa5b2af9e; cjConsent=MHxOfDB8Tnww; cjUser=0584478d-0330-42a6-a747-c755d01e97c5; _axwrt=231dbf38-99ac-43c0-b613-bb18c2bb4ec6; __podscribe_wayfair_referrer=_; __podscribe_wayfair_landing_url=https://www.wayfair.com/rugs/pdp/bungalow-rose-oriental-boho-vintage-print-machine-washable-area-rug-maroon-red-low-pile-high-with-non-slip-backing-for-high-traffic-area-w111359465.html?piid=242722570; __podscribe_did=pscrb_3324b67a-4673-4cca-c172-b5d5c6058533; rskxRunCookie=0; rCookie=z3siebrhcgrbb06zee4wysm7wlknml; _tt_enable_cookie=1; _ttp=01JNMD0R02FPHJG14NWP9N8WAY_.tt.1; __attentive_id=f1f779439ec14f528531d03c489026c0; __attentive_cco=1741220241790; axwrt=231dbf38-99ac-43c0-b613-bb18c2bb4ec6; attntv_mstore_email=a249022968@gmail.com:0; CSN_RT=9566856C04E58E1EA219C707E4BBB5BEC061732B5EDA406D9F4BE3B7FD464614; CSNID=9C769B99-F64C-4B2B-92BB-BEA485225AA3; WFCS=CS3; __attentive_client_user_id=0e39ce9f145fe192ddf13172fc8758d4461db31ae5ed2a9c1b0f39f5cf3ec6a1; _alby_user=76daa402-04af-422f-bc78-ad04e032610a; _ga_Q0HJWP456J=deleted; _ga_0GV7WXFNMT=deleted; _uetvid=56c2f9b0fa2011efb07fd7c1d99fb8a7; ndp_session_id=f75cbd2e-2780-4e5a-9c5a-19abf454819a; ibb=1; postalCode=67346; SFSID=6384f0bbb3246c8a987824d6b0af8c7f; serverUAInfo=%7B%22browser%22%3A%22Google%20Chrome%22%2C%22browserVersion%22%3A136%2C%22OS%22%3A%22Windows%22%2C%22OSVersion%22%3A%22%22%2C%22isMobile%22%3Afalse%2C%22isTablet%22%3Afalse%2C%22isTouch%22%3Afalse%7D; pxcts=6197c0c5-3065-11f0-beb4-c7213f7e90cd; IR_gbd=wayfair.com; _gid=GA1.2.27009705.1747614611; _ga_0GV7WXFNMT=deleted; _ga_Q0HJWP456J=deleted; canary=0; _gcl_au=1.1.417332783.1741220240.1295446020.1748308354.1748308429; _pxhd=Nv3Yuo7nF6tEUtjkAO7AxcB8YwKbvBrDOv2z2xBrCmCyzhEy1rS5mlavQkhr7htQjRfo5CQb6fH1kIeTpr6sbg==:nFAF2M4p0JGgv6g2EWKSq6qSp8inUBtURHAKByKAner2MHjUecBmhzQ/-P2QAOe/wea7IEitTn1JnjGmE4PZJtiusAMbqaYPTu1fbyWperA=; CSN_CSRF=66c5ff8ebc99cf28d65700146c1eb0ad15ae16dfe94265aedf2e4bc0a322f93b; __attentive_dv=1; vid=56d9465d-0629-4e53-8489-443bb705e641; WFDC=DSM; CSN_CT=eyJhbGciOiJSUzI1NiIsImtpZCI6InBlRG5BMWVVVGRVQU00YVdjU3FnZm40ZEJhbFZCYnJ4R2ZEU0ZQYXVQbG8iLCJ4NXQiOiJJMkJNSDFJREVoUUVmamNtdDZrcU02d3BiME0iLCJ0eXAiOiJKV1QiLCJqa3UiOiJodHRwczovL3Nzby5hdXRoLndheWZhaXIuY29tLy53ZWxsLWtub3duL29wZW5pZC1jb25maWd1cmF0aW9uL2p3a3MifQ.eyJuYmYiOjE3NDg0MTQ0NjUsImV4cCI6MTc0ODQyODg2NiwiaWF0IjoxNzQ4NDE0NDY2LCJpc3MiOiJodHRwczovL3Nzby5hdXRoLndheWZhaXIuY29tLyIsImF1ZCI6ImF1dGhfaWRlbnRpdHkiLCJjbGllbnRfaWQiOiJ5NnZVV0dUd2dFVlA0VEFZbXZuTGxBIiwiY3VpZCI6IjYxNzQxMTc5MTMiLCJzdWIiOiIzMDk0MjQxMTAiLCJ2ZXJzaW9uIjoiMi4wIiwicGx0Ijoid2ViIiwib3JpZ2luYWxfaWF0IjoiMTc0NDE2MzIwNyIsInJvbGUiOiJzZjpjdXN0b21lciIsImp0aSI6IjY0MEIyOTk1N0U1QUEwMENGNUQ5MzA0MDREQzdFQUNBIiwic2NvcGUiOiJvcGVuaWQgb2ZmbGluZV9hY2Nlc3Mgc2Y6cmVjb2duaXplZCBzZjp0cnVzdGVkIiwiYW1yIjpbImNyZWF0ZV91c2VyIiwicmVmcmVzaCJdfQ.TNwu4B8iFUzGatD-DxuPWU8HC7dqOlZEyJvAqjrFWDmKVYrKFPZm9dzzyFcVFyun9rNEmBl7XgRrwR45gIVzdkr2TI_OktsMuD-r_TuzUxWr4rdaITaoCJdivA2EuZwsob2Od-evfZ6apCIXB-pmH6iWEIxr3QNbf5OqXMCoJnEVeU8cFxBKUwodX72lRX1dRWxZ40bvp48bLf_mCipPZRDI_k6Hu995r2CGXMF2U9Ud6UwrfB_648451UZwdHICvUtt-0fC3Rn12ZMFKxEkXuUAwy8K4wH3H2VD6J5D5W5VfpUh0j_XxNh5hBmOTQsoNp4JOS57gCsrPk8cbH0LRvffivDn8U5OurYUYjoipH6n5-rw8W-mGNwAd3wsq9aObIYo_AoANPCS4TE88pXiTyun7CtdlMSicUjV25ye5eZSBeSjnN7WvHvXvFuH2SKMKe1Rt5CBV25IMNGI71nkOhterKyrPgQeDYDg-w--VHKvdja3xG7clfTl7HvW-r8o1VSAnRWvRyfCP5IJyBOD3OMYH3falk7o18YNZUnLVTfFkqPOdViOZFYds7bDXJS2cgDL3CPlZ9W1nJgnDo_PK-E3DkBXnPPO_IBgej5G9eMEEt49WhrEYhEOUFIu1GSXqgocwXAzVZRyi60Ds1dv6VTKZBj1zVb49xBsgfR1neA; __attentive_session_id=faa36bb136e343c099d0a7914b8c141c; __attentive_ss_referrer=ORGANIC; _px3=d5ec0bfabd958951a546d032b45a5586114f05f440151be0d5ed8aedb96e62ac:hGnmqBX7H4yvqbWapdmN3bAHz6KhqkxrtsOkI+Drqy+HpeEKaWF028+G5k6do+Vgt77cUn6Pn93fmAgig/iTBg==:1000:I9CxbeOJUQzM11XcAln1JFLbT1jOnO7+AVIHzwneKOPLWzv0J+ijWInZKzFJnQ70c9zKZFnK4dBPBBpgH38HlSbbjBbWwje/v0XDyYcFsAPQRncH8U3qtZITor7/O7nHktdFOM3Qqwar6Csi1becFvp8IH4g8rXoQqcaydOv8NXpg11HSomcRM/uiljfygc/GJyEYYulOhI7Or45ytL4mUCGTQHJrEvALCzE6aJ8CCA=; otx=IuTn+7zQTna6mdd5KRGoVw==; __wid=503578700; ax_visitor=%7B%22firstVisitTs%22%3A1741220225682%2C%22lastVisitTs%22%3A1748403702408%2C%22currentVisitStartTs%22%3A1748414464937%2C%22ts%22%3A1748421674962%2C%22visitCount%22%3A103%7D; _rdt_uuid=1741220227124.e1710325-d83d-4119-a820-5cc7a3c12483; _rdt_em=0e39ce9f145fe192ddf13172fc8758d4461db31ae5ed2a9c1b0f39f5cf3ec6a1:0e39ce9f145fe192ddf13172fc8758d4461db31ae5ed2a9c1b0f39f5cf3ec6a1; _uetsid=0671d4c0344e11f0a1d469c877b3b8d7; forterToken=5349ac441e664549a50d947c6faa35fd_1748421664547_5706_UDF43-mnf-a4_25ck_REluqn+URlE%3D-1962-v2; forterToken=5349ac441e664549a50d947c6faa35fd_1748421664547_5706_UDF43-mnf-a4_25ck_REluqn+URlE%3D-1962-v2; IR_12051=1748421680314%7C0%7C1748421680314%7C%7C; IR_PI=3c3e4f6a-14e8-11f0-8c2a-a5fe5042a2dc%7C1748421680314; lastRskxRun=1748421681343; _ga_0GV7WXFNMT=GS2.1.s1748420911$o184$g1$t1748421683$j15$l0$h0; CSNPersist=page_of_visit%3D2013; _attn_=eyJ1Ijoie1wiY29cIjoxNzQxMjIwMjQxNzg5LFwidW9cIjoxNzQxMjIwMjQxNzg5LFwibWFcIjoyMTkwMCxcImluXCI6ZmFsc2UsXCJ2YWxcIjpcImYxZjc3OTQzOWVjMTRmNTI4NTMxZDAzYzQ4OTAyNmMwXCJ9Iiwic2VzIjoie1widmFsXCI6XCJmYWEzNmJiMTM2ZTM0M2MwOTlkMGE3OTE0YjhjMTQxY1wiLFwidW9cIjoxNzQ4NDIxNjg1NTcxLFwiY29cIjoxNzQ4NDIxNjg1NTcxLFwibWFcIjowLjAyMDgzMzMzMzMzMzMzMzMzMn0ifQ==; _gat_gtag_UA_2081664_4=1; _ga_Q0HJWP456J=GS2.1.s1748420911$o179$g1$t1748421686$j12$l0$h0; _ga=GA1.1.1847679220.1741220240; ttcsid=1748420908738::XgSOmwkwvYLac8ld8Fm0.159.1748421688634; ttcsid_C7KTM4O68TKN71DEGAK0=1748420908735::VIr-v6vX2gmMibnd9CoB.157.1748421688866; __attentive_pv=3',
    }


    params = {
        'hash': 'a636f23a2ad15b342db756fb5e0ea093',
    }
    sku = sku.upper()
    datas = []
    for i in range(1, 41):
        json_data = {
            'variables': {
                'sku': sku,
                'sort_order': 'RELEVANCE',
                'page_number': i,
                'filter_rating': '',
                'reviews_per_page': 0,
                'search_query': '',
                'language_code': 'en',
            },
        }
        try:
            response = requests.post('https://www.wayfair.com/graphql', params=params, cookies=cookies, headers=headers, json=json_data)
            json_data = response.json()
        except:
            #error_msg()
            import pdb;pdb.set_trace()
            pass
        print(sku, "page_number =", i, "len =", len(json_data['data']['product']['customerReviews']['reviews']))
        datas += json_data['data']['product']['customerReviews']['reviews']
        if len(json_data['data']['product']['customerReviews']['reviews']) < 10:
            break
        #import time;time.sleep(2)
        #import pdb;pdb.set_trace()
        pass
    json_save_path = r'D:\rpa_tools\playwright_demo\wayfair\reviews'
    if len(datas) > 0:
        df = pd.DataFrame(datas)
        df.to_excel(json_save_path + "/" + sku + '.xlsx')
    pass

def set_options(x):
    import ast
    return ast.literal_eval(x)[0]['name'] + ":" + ast.literal_eval(x)[0]['value'] if len(ast.literal_eval(x)) > 0 else ''

def customerPhotos(x):
    import ast
    return ast.literal_eval(x)[0]['src'] if len(ast.literal_eval(x)) > 0 else ''
def trans_time(x):
    from dateutil import parser
    return parser.parse(x).strftime("%Y-%m-%d %H:%M:%S")

def read_excel(excel_file_path, sku):
    import pandas as pd
    import datetime
    datetime_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        df = pd.read_excel(excel_file_path)
    except:
        df = pd.read_csv(excel_file_path)
        if 'Review Id' not in df.keys():
            import pdb;pdb.set_trace()
            pass
    cls = ['review_id', 'reviewer_name', 'rating', 'comment', 'comment_time', 'images', 'options', 'review_helpful', 'reviewer_location', 'scraped_at']
    if 'Review Id' not in df.keys():
        df = df[['reviewId', 'reviewerName', 'ratingStars', 'productComments', 'date', 'customerPhotos', 'options', 'reviewHelpful', 'reviewerLocation']]
        df['scraped_at'] = datetime_now
        df['ratingStars'] = df['ratingStars'].apply(lambda x: int(x / 2))
        
        df['reviewHelpful'] = df['reviewHelpful'].astype(str)
        df['reviewHelpful'] = df['reviewHelpful'] = df.apply(lambda row: '0' if str(row['reviewHelpful']) == 'nan' else str(row['reviewHelpful']), axis=1)
        df['options'] = df['options'].apply(set_options)
        df['customerPhotos'] = df['customerPhotos'].apply(customerPhotos)
        df.columns = ['review_id', 'reviewer_name', 'rating', 'comment', 'comment_time', 'images', 'options', 'review_helpful', 'reviewer_location', 'scraped_at']
        pass
    else:
        df.columns = ['review_id', 'reviewer_name', 'rating', 'comment', 'comment_time', 'images', 'options', 'review_helpful', 'reviewer_location', 'scraped_at']
        df['scraped_at'] = df['scraped_at'].apply(trans_time)
        df['review_helpful'] = df['review_helpful'].apply(lambda x: '1' if str(x) == 'Yes' else '0')
        #import pdb;pdb.set_trace()
        #df.rename(columns={'A':'a', 'B':'b', 'C':'c'}, inplace = True)
        pass
    df['sku'] = sku
    for cl in cls:
        df[cl] = df[cl].astype(str)
    #import pdb;pdb.set_trace()
    return df


import os
import pandas as pd
excel_path = r'D:\rpa_tools\playwright_demo\wayfair'
df = pd.read_excel(excel_path + "\datas_v5.xlsx")
lines = open("urls.txt").readlines()
lines = []
excel_urls = []
for i in range(len(df)):
    excel_urls.append(df.loc[i, 'url'])
excel_urls.reverse()
for url in excel_urls:
    lines.append(url)
path = r'D:\rpa_tools\playwright_demo\wayfair\reviews\\'
file_list = []
for excel_file in os.listdir(path):
    if excel_file.endswith(".xlsx"):
        file_list.append(excel_file)
file_str = ",".join(file_list)
count = 1
has_count = 0
df = pd.DataFrame()
for line in lines:
    line = line.strip()
    #print(line)
    file_name = line.replace("https://", "").replace("/", "_").replace("?", "#") + ".xlsx"
    # if os.path.exists(path + file_name):
    #     has_count += 1
    #     continue
    # if file_str.find(file_name[-100:]) >= 0:
    #     has_count += 1
    #     continue
    # if file_str.find(file_name.split(".html")[0]) >= 0:
    #     has_count += 1
    #     continue
    sku = line.split(".html")[0].split("-")[-1].upper()
    if file_str.find(sku) >= 0:
        print(sku)
        if not os.path.exists(path + sku + ".xlsx"):
            import pdb;pdb.set_trace()
            pass
        ret_df = read_excel(path + sku + ".xlsx", sku)
        df = pd.concat([df, ret_df], ignore_index=True)
        has_count += 1
        continue
    print('count =', count, 'has_count = ', has_count)
    print(file_name)
    print(line)
    import datetime
    print(datetime.datetime.now())
    count += 1
    #import pdb;pdb.set_trace()
    get_reviews_by_url(sku)
    pass
    #print(file_name[-100:])
print("has_count =", has_count)
import pdb;pdb.set_trace()
df.to_excel("./res_data.xlsx", index=False)