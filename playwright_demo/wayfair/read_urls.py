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
        'WFDC': 'DSM',
        'vid': '56d9465d-0629-4e53-8489-443bb705e641',
        'CSN_CT': 'eyJhbGciOiJSUzI1NiIsImtpZCI6InBlRG5BMWVVVGRVQU00YVdjU3FnZm40ZEJhbFZCYnJ4R2ZEU0ZQYXVQbG8iLCJ4NXQiOiI4OV9HLVpaMWZyajdKcXZrZVNzaXJqc3RyRUUiLCJ0eXAiOiJKV1QiLCJqa3UiOiJodHRwczovL3Nzby5hdXRoLndheWZhaXIuY29tLy53ZWxsLWtub3duL29wZW5pZC1jb25maWd1cmF0aW9uL2p3a3MifQ.eyJuYmYiOjE3NDgzOTYzNjksImV4cCI6MTc0ODQxMDc3MCwiaWF0IjoxNzQ4Mzk2MzcwLCJpc3MiOiJodHRwczovL3Nzby5hdXRoLndheWZhaXIuY29tLyIsImF1ZCI6ImF1dGhfaWRlbnRpdHkiLCJjbGllbnRfaWQiOiJ5NnZVV0dUd2dFVlA0VEFZbXZuTGxBIiwiY3VpZCI6IjYxNzQxMTc5MTMiLCJzdWIiOiIzMDk0MjQxMTAiLCJ2ZXJzaW9uIjoiMi4wIiwicGx0Ijoid2ViIiwib3JpZ2luYWxfaWF0IjoiMTc0NDE2MzIwNyIsInJvbGUiOiJzZjpjdXN0b21lciIsImp0aSI6IkRGRDU4NEI5QkI2ODUwMTc5RDczNkU1MjBDRkYxMTAyIiwic2NvcGUiOiJvcGVuaWQgb2ZmbGluZV9hY2Nlc3Mgc2Y6cmVjb2duaXplZCBzZjp0cnVzdGVkIiwiYW1yIjpbImNyZWF0ZV91c2VyIiwicmVmcmVzaCJdfQ.VUUk4zvbbeADyp_qUVhVGgzN7AM_OKdYt9Lab-BnC5QKV38PFnqXZcTd_dqbwMTge-vt8wSI9bwkR-2vcJs1CHi3ShTSxkhdBXNiAXnZIYVwoDujzlnJuCqSaLMXgLtSCHa3GHOjV8gSeb2Tx7-Dw3DpXfP4ayotJzwvo5Xri6A2beAs3iq88ROAAVuwTxxCrJeuxnmSVg_64SwovNQgTvzvTVJOwwbjwExXZ9JGLsZuG5y-SpQbN2diPwWsh9qsbFBpCYEa6_s2TF8rI6gv1E4MMYWvcc4AY5TozJKQSM3X95uHe93rCpaNE0_ThiOHYZOOfAUqft3MLo-EKlNOCyMwcDb78eBdwbnKsNaaguJ-yYJvveRVbReEXh4bJVWul0hYuHLBIh73ZkOu2xDup1Up2pWe_c-NataZvpHiwyTTHYoevRBf3s_SYY1a32bsNZvSHXX6b1lpVlm1BeO8VSO-T7ABySQVToKloVTD2muLPBpcRXMh0NEKIgcrMHaO_05pSLL4siiSmk7wdzXtug1CX-HQoqIt1f2sgavA2sLYcosc_6OVMlOE8jgpvYs7cIS1wmg3Zfip6-mK5tjoVQ_LWLpz4Wjwcg1AZgd2vEe7r1Va3L5-6kTLIVNbnC0uEkjpKTnQuCCf_koX9G0sFIe9b7EFXfBvsNVXdlEr5L4',
        '__wid': '981894470',
        '__attentive_session_id': '9c03a7f015f04512aae6422954390574',
        '__attentive_ss_referrer': 'ORGANIC',
        '_gat_gtag_UA_2081664_4': '1',
        'otx': 'B7/Su6LmQP2HzrOwdnoVcQ==',
        '_px3': 'b6020d5b7c9c0e022d38f3241d81f427c568da3b67bbf8bb49c3cdfb6bebf2bd:J9gGe9BjowrJ7EgB/o/sRtsOhTkNAJZ7FDn+niTX27I0m5EFa9V/lsLudgWMULmsCtP/E/+DHaNoIoYI1vnAPA==:1000:43FSOU9aQtXuBwWGbbZLXk0UoJWruV58xR7gHRdI13v3Lwo3E4FmsFpkeVermcXdEpZW38lsQ3WJTYk/K+LfAk8vdD+upY0bC2+f3L3/k7+gzX4jOWHZefPHJ9dkfPBAKM9/PTsl/SC6A5NcQgSkBVz1sp7ylPaWy6txjSe/smV5+e4DK5h9fZFVXDigsxxu4BS/77CgIUv1MQ/JgwaMKUCzAqRT9Mwy8XxnQjZMEU4=',
        '_attn_': 'eyJ1Ijoie1wiY29cIjoxNzQxMjIwMjQxNzg5LFwidW9cIjoxNzQxMjIwMjQxNzg5LFwibWFcIjoyMTkwMCxcImluXCI6ZmFsc2UsXCJ2YWxcIjpcImYxZjc3OTQzOWVjMTRmNTI4NTMxZDAzYzQ4OTAyNmMwXCJ9Iiwic2VzIjoie1widmFsXCI6XCI5YzAzYTdmMDE1ZjA0NTEyYWFlNjQyMjk1NDM5MDU3NFwiLFwidW9cIjoxNzQ4NDAzNzU2NDQxLFwiY29cIjoxNzQ4NDAzNzU2NDQxLFwibWFcIjowLjAyMDgzMzMzMzMzMzMzMzMzMn0ifQ==',
        'CSNPersist': 'page_of_visit%3D1958',
        '_ga_0GV7WXFNMT': 'GS2.1.s1748403703$o181$g1$t1748403757$j6$l0$h0',
        '__attentive_pv': '2',
        '_uetsid': '0671d4c0344e11f0a1d469c877b3b8d7',
        'ax_visitor': '%7B%22firstVisitTs%22%3A1741220225682%2C%22lastVisitTs%22%3A1748396381531%2C%22currentVisitStartTs%22%3A1748403702408%2C%22ts%22%3A1748403759115%2C%22visitCount%22%3A102%7D',
        '_rdt_uuid': '1741220227124.e1710325-d83d-4119-a820-5cc7a3c12483',
        '_rdt_em': '0e39ce9f145fe192ddf13172fc8758d4461db31ae5ed2a9c1b0f39f5cf3ec6a1:0e39ce9f145fe192ddf13172fc8758d4461db31ae5ed2a9c1b0f39f5cf3ec6a1',
        'lastRskxRun': '1748403759269',
        'IR_12051': '1748403759282%7C0%7C1748403759282%7C%7C',
        '_ga_Q0HJWP456J': 'GS2.1.s1748403703$o176$g1$t1748403760$j3$l0$h0',
        '_ga': 'GA1.1.1847679220.1741220240',
        'IR_PI': '3c3e4f6a-14e8-11f0-8c2a-a5fe5042a2dc%7C1748403759282',
        'ttcsid': '1748403712916::gg5F7Yl-wwjazzqDMguZ.156.1748403761326',
        'forterToken': '5349ac441e664549a50d947c6faa35fd_1748403756290_5706_UDF43-m4_25ck_/w6fYENPzeA%3D-13496-v2',
        'forterToken': '5349ac441e664549a50d947c6faa35fd_1748403756290_5706_UDF43-m4_25ck_/w6fYENPzeA%3D-13496-v2',
        'ttcsid_C7KTM4O68TKN71DEGAK0': '1748403712915::Q_p36Jx6NbsOtXC2FwO3.154.1748403761930',
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
        'referer': 'https://www.wayfair.com/rugs/pdp/ophelia-co-holden-traditional-tiled-power-loom-performance-beigecream-rug-w002339053.html?piid=1719953789&auctionId=96376cac-0ea3-484a-8f10-980d4e2405b0&adTypeId=1',
        'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'use-web-hash': 'true',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        'x-parent-txid': '2E98y1MXSQqMxVKuCgn09g==',
        # 'cookie': 'CSNUtId=89b316d1-cb83-48f9-a3a0-993c5c25092e; i18nPrefs=lang%3Den-US; ExCSNUtId=89b316d1-cb83-48f9-a3a0-993c5c25092e; _pxvid=2f37446f-fa20-11ef-b233-483ed9754125; __pxvid=2fc9176f-fa20-11ef-8c6f-0242ac120002; salsify_session_id=b1e1d55f-19be-48fc-85bc-c62b20aa0a35; __ssid=d5fb35a47d5613d1c8309ffa5b2af9e; cjConsent=MHxOfDB8Tnww; cjUser=0584478d-0330-42a6-a747-c755d01e97c5; _axwrt=231dbf38-99ac-43c0-b613-bb18c2bb4ec6; __podscribe_wayfair_referrer=_; __podscribe_wayfair_landing_url=https://www.wayfair.com/rugs/pdp/bungalow-rose-oriental-boho-vintage-print-machine-washable-area-rug-maroon-red-low-pile-high-with-non-slip-backing-for-high-traffic-area-w111359465.html?piid=242722570; __podscribe_did=pscrb_3324b67a-4673-4cca-c172-b5d5c6058533; rskxRunCookie=0; rCookie=z3siebrhcgrbb06zee4wysm7wlknml; _tt_enable_cookie=1; _ttp=01JNMD0R02FPHJG14NWP9N8WAY_.tt.1; __attentive_id=f1f779439ec14f528531d03c489026c0; __attentive_cco=1741220241790; axwrt=231dbf38-99ac-43c0-b613-bb18c2bb4ec6; attntv_mstore_email=a249022968@gmail.com:0; CSN_RT=9566856C04E58E1EA219C707E4BBB5BEC061732B5EDA406D9F4BE3B7FD464614; CSNID=9C769B99-F64C-4B2B-92BB-BEA485225AA3; WFCS=CS3; __attentive_client_user_id=0e39ce9f145fe192ddf13172fc8758d4461db31ae5ed2a9c1b0f39f5cf3ec6a1; _alby_user=76daa402-04af-422f-bc78-ad04e032610a; _ga_Q0HJWP456J=deleted; _ga_0GV7WXFNMT=deleted; _uetvid=56c2f9b0fa2011efb07fd7c1d99fb8a7; ndp_session_id=f75cbd2e-2780-4e5a-9c5a-19abf454819a; ibb=1; postalCode=67346; SFSID=6384f0bbb3246c8a987824d6b0af8c7f; serverUAInfo=%7B%22browser%22%3A%22Google%20Chrome%22%2C%22browserVersion%22%3A136%2C%22OS%22%3A%22Windows%22%2C%22OSVersion%22%3A%22%22%2C%22isMobile%22%3Afalse%2C%22isTablet%22%3Afalse%2C%22isTouch%22%3Afalse%7D; pxcts=6197c0c5-3065-11f0-beb4-c7213f7e90cd; IR_gbd=wayfair.com; _gid=GA1.2.27009705.1747614611; _ga_0GV7WXFNMT=deleted; _ga_Q0HJWP456J=deleted; canary=0; _gcl_au=1.1.417332783.1741220240.1295446020.1748308354.1748308429; _pxhd=Nv3Yuo7nF6tEUtjkAO7AxcB8YwKbvBrDOv2z2xBrCmCyzhEy1rS5mlavQkhr7htQjRfo5CQb6fH1kIeTpr6sbg==:nFAF2M4p0JGgv6g2EWKSq6qSp8inUBtURHAKByKAner2MHjUecBmhzQ/-P2QAOe/wea7IEitTn1JnjGmE4PZJtiusAMbqaYPTu1fbyWperA=; CSN_CSRF=66c5ff8ebc99cf28d65700146c1eb0ad15ae16dfe94265aedf2e4bc0a322f93b; __attentive_dv=1; WFDC=DSM; vid=56d9465d-0629-4e53-8489-443bb705e641; CSN_CT=eyJhbGciOiJSUzI1NiIsImtpZCI6InBlRG5BMWVVVGRVQU00YVdjU3FnZm40ZEJhbFZCYnJ4R2ZEU0ZQYXVQbG8iLCJ4NXQiOiI4OV9HLVpaMWZyajdKcXZrZVNzaXJqc3RyRUUiLCJ0eXAiOiJKV1QiLCJqa3UiOiJodHRwczovL3Nzby5hdXRoLndheWZhaXIuY29tLy53ZWxsLWtub3duL29wZW5pZC1jb25maWd1cmF0aW9uL2p3a3MifQ.eyJuYmYiOjE3NDgzOTYzNjksImV4cCI6MTc0ODQxMDc3MCwiaWF0IjoxNzQ4Mzk2MzcwLCJpc3MiOiJodHRwczovL3Nzby5hdXRoLndheWZhaXIuY29tLyIsImF1ZCI6ImF1dGhfaWRlbnRpdHkiLCJjbGllbnRfaWQiOiJ5NnZVV0dUd2dFVlA0VEFZbXZuTGxBIiwiY3VpZCI6IjYxNzQxMTc5MTMiLCJzdWIiOiIzMDk0MjQxMTAiLCJ2ZXJzaW9uIjoiMi4wIiwicGx0Ijoid2ViIiwib3JpZ2luYWxfaWF0IjoiMTc0NDE2MzIwNyIsInJvbGUiOiJzZjpjdXN0b21lciIsImp0aSI6IkRGRDU4NEI5QkI2ODUwMTc5RDczNkU1MjBDRkYxMTAyIiwic2NvcGUiOiJvcGVuaWQgb2ZmbGluZV9hY2Nlc3Mgc2Y6cmVjb2duaXplZCBzZjp0cnVzdGVkIiwiYW1yIjpbImNyZWF0ZV91c2VyIiwicmVmcmVzaCJdfQ.VUUk4zvbbeADyp_qUVhVGgzN7AM_OKdYt9Lab-BnC5QKV38PFnqXZcTd_dqbwMTge-vt8wSI9bwkR-2vcJs1CHi3ShTSxkhdBXNiAXnZIYVwoDujzlnJuCqSaLMXgLtSCHa3GHOjV8gSeb2Tx7-Dw3DpXfP4ayotJzwvo5Xri6A2beAs3iq88ROAAVuwTxxCrJeuxnmSVg_64SwovNQgTvzvTVJOwwbjwExXZ9JGLsZuG5y-SpQbN2diPwWsh9qsbFBpCYEa6_s2TF8rI6gv1E4MMYWvcc4AY5TozJKQSM3X95uHe93rCpaNE0_ThiOHYZOOfAUqft3MLo-EKlNOCyMwcDb78eBdwbnKsNaaguJ-yYJvveRVbReEXh4bJVWul0hYuHLBIh73ZkOu2xDup1Up2pWe_c-NataZvpHiwyTTHYoevRBf3s_SYY1a32bsNZvSHXX6b1lpVlm1BeO8VSO-T7ABySQVToKloVTD2muLPBpcRXMh0NEKIgcrMHaO_05pSLL4siiSmk7wdzXtug1CX-HQoqIt1f2sgavA2sLYcosc_6OVMlOE8jgpvYs7cIS1wmg3Zfip6-mK5tjoVQ_LWLpz4Wjwcg1AZgd2vEe7r1Va3L5-6kTLIVNbnC0uEkjpKTnQuCCf_koX9G0sFIe9b7EFXfBvsNVXdlEr5L4; __wid=981894470; __attentive_session_id=9c03a7f015f04512aae6422954390574; __attentive_ss_referrer=ORGANIC; _gat_gtag_UA_2081664_4=1; otx=B7/Su6LmQP2HzrOwdnoVcQ==; _px3=b6020d5b7c9c0e022d38f3241d81f427c568da3b67bbf8bb49c3cdfb6bebf2bd:J9gGe9BjowrJ7EgB/o/sRtsOhTkNAJZ7FDn+niTX27I0m5EFa9V/lsLudgWMULmsCtP/E/+DHaNoIoYI1vnAPA==:1000:43FSOU9aQtXuBwWGbbZLXk0UoJWruV58xR7gHRdI13v3Lwo3E4FmsFpkeVermcXdEpZW38lsQ3WJTYk/K+LfAk8vdD+upY0bC2+f3L3/k7+gzX4jOWHZefPHJ9dkfPBAKM9/PTsl/SC6A5NcQgSkBVz1sp7ylPaWy6txjSe/smV5+e4DK5h9fZFVXDigsxxu4BS/77CgIUv1MQ/JgwaMKUCzAqRT9Mwy8XxnQjZMEU4=; _attn_=eyJ1Ijoie1wiY29cIjoxNzQxMjIwMjQxNzg5LFwidW9cIjoxNzQxMjIwMjQxNzg5LFwibWFcIjoyMTkwMCxcImluXCI6ZmFsc2UsXCJ2YWxcIjpcImYxZjc3OTQzOWVjMTRmNTI4NTMxZDAzYzQ4OTAyNmMwXCJ9Iiwic2VzIjoie1widmFsXCI6XCI5YzAzYTdmMDE1ZjA0NTEyYWFlNjQyMjk1NDM5MDU3NFwiLFwidW9cIjoxNzQ4NDAzNzU2NDQxLFwiY29cIjoxNzQ4NDAzNzU2NDQxLFwibWFcIjowLjAyMDgzMzMzMzMzMzMzMzMzMn0ifQ==; CSNPersist=page_of_visit%3D1958; _ga_0GV7WXFNMT=GS2.1.s1748403703$o181$g1$t1748403757$j6$l0$h0; __attentive_pv=2; _uetsid=0671d4c0344e11f0a1d469c877b3b8d7; ax_visitor=%7B%22firstVisitTs%22%3A1741220225682%2C%22lastVisitTs%22%3A1748396381531%2C%22currentVisitStartTs%22%3A1748403702408%2C%22ts%22%3A1748403759115%2C%22visitCount%22%3A102%7D; _rdt_uuid=1741220227124.e1710325-d83d-4119-a820-5cc7a3c12483; _rdt_em=0e39ce9f145fe192ddf13172fc8758d4461db31ae5ed2a9c1b0f39f5cf3ec6a1:0e39ce9f145fe192ddf13172fc8758d4461db31ae5ed2a9c1b0f39f5cf3ec6a1; lastRskxRun=1748403759269; IR_12051=1748403759282%7C0%7C1748403759282%7C%7C; _ga_Q0HJWP456J=GS2.1.s1748403703$o176$g1$t1748403760$j3$l0$h0; _ga=GA1.1.1847679220.1741220240; IR_PI=3c3e4f6a-14e8-11f0-8c2a-a5fe5042a2dc%7C1748403759282; ttcsid=1748403712916::gg5F7Yl-wwjazzqDMguZ.156.1748403761326; forterToken=5349ac441e664549a50d947c6faa35fd_1748403756290_5706_UDF43-m4_25ck_/w6fYENPzeA%3D-13496-v2; forterToken=5349ac441e664549a50d947c6faa35fd_1748403756290_5706_UDF43-m4_25ck_/w6fYENPzeA%3D-13496-v2; ttcsid_C7KTM4O68TKN71DEGAK0=1748403712915::Q_p36Jx6NbsOtXC2FwO3.154.1748403761930',
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
        response = requests.post('https://www.wayfair.com/graphql', params=params, cookies=cookies, headers=headers, json=json_data)
        json_data = response.json()
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

import os
import pandas as pd
excel_path = r'D:\rpa_tools\playwright_demo\wayfair'
df = pd.read_excel(excel_path + "\datas_v5.xlsx")
lines = open("urls.txt").readlines()
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
for line in lines:
    line = line.strip()
    #print(line)
    file_name = line.replace("https://", "").replace("/", "_").replace("?", "#") + ".xlsx"
    if os.path.exists(path + file_name):
        has_count += 1
        continue
    if file_str.find(file_name[-100:]) >= 0:
        has_count += 1
        continue
    if file_str.find(file_name.split(".html")[0]) >= 0:
        has_count += 1
        continue
    sku = line.split(".html")[0].split("-")[-1]
    if file_str.find(sku.upper()) >= 0:
        has_count += 1
        continue
    print('count =', count, 'has_count = ', has_count)
    print(file_name)
    print(line)
    count += 1
    #import pdb;pdb.set_trace()
    get_reviews_by_url(sku)
    pass
    #print(file_name[-100:])