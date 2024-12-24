import requests

cookies = {
    'session-id': '146-5611030-1559043',
    'i18n-prefs': 'USD',
    'lc-main': 'zh_CN',
    'sp-cdn': '"L5Z9:HK"',
    'ubid-main': '133-6238693-6854259',
    'session-id-time': '2082787201l',
    'session-token': 'NdRhZayMSXHo9No30GlfZzsReMENk92Soo1ORBckBq2bacfWVVdy7+0MZKb+PjG2cOY1szXLoHozMjfMz9ArTZPa/VoHXfO4ItJ2MB5aarKu5q44775XybAeuRNo12jQOvucIx7M6XVXbkHJVsM93ONCoBSj06AohajkOBK/pxaBmEd5+OEByeGI41qjoZLlM1t+1lxVrqP8zH6vu43GIV7RMl044ArhKl5l6q4jq90uiUgGONIw7OsFg3Ks95lhZeudSRorLOJrm3BWD7BajtHCspdltVSVSnHgeCSa4AoP9N1QK7igKcqBdA5m3gpbNz5QLoDDhgC6AW461M93Mu6xP+4wqhUj',
}

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'text/plain;charset=UTF-8',
    # 'cookie': 'session-id=146-5611030-1559043; i18n-prefs=USD; lc-main=zh_CN; sp-cdn="L5Z9:HK"; ubid-main=133-6238693-6854259; session-id-time=2082787201l; session-token=NdRhZayMSXHo9No30GlfZzsReMENk92Soo1ORBckBq2bacfWVVdy7+0MZKb+PjG2cOY1szXLoHozMjfMz9ArTZPa/VoHXfO4ItJ2MB5aarKu5q44775XybAeuRNo12jQOvucIx7M6XVXbkHJVsM93ONCoBSj06AohajkOBK/pxaBmEd5+OEByeGI41qjoZLlM1t+1lxVrqP8zH6vu43GIV7RMl044ArhKl5l6q4jq90uiUgGONIw7OsFg3Ks95lhZeudSRorLOJrm3BWD7BajtHCspdltVSVSnHgeCSa4AoP9N1QK7igKcqBdA5m3gpbNz5QLoDDhgC6AW461M93Mu6xP+4wqhUj',
    'origin': 'https://www.amazon.com',
    'pragma': 'no-cache',
    'priority': 'u=4, i',
    'referer': 'https://www.amazon.com/',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}

data = '{"rid":"W0TPJMDT84AZMF2KKHAN","sid":"146-5611030-1559043","mid":"ATVPDKIKX0DER","sn":"www.amazon.com","reqs":[{"cap-ciba":{"k":"fwcim","r":"W0TPJMDT84AZMF2KKHAN","p":"https://www.amazon.com/cart/ref=ord_cart_shr?app-nav-type=none&dc=df","c":null,"t":1734948771746,"type":"inc","md":"ECdITeCs:U5sTyGRIFFlj/en0hg9RMrMyn4Pz1L/ETNedrhlArFXs7Hd48RrazUF/uQ6MoUIIFoQbAoXFrTB6VIJdwU68iRURKxfjED+FPbhFdXOroK5zlynrKvNNNdkduY9L2PSCLCKqSrz1Y4heq64WGytRyo0X7xJMYCJx07EKxTaOC5bgjnQD0phNhDsL1nowPic+"}},{"cap-ciba":{"k":"fwcim","r":"W0TPJMDT84AZMF2KKHAN","p":"https://www.amazon.com/cart/ref=ord_cart_shr?app-nav-type=none&dc=df","c":null,"t":1734948776747,"type":"inc","md":"ECdITeCs:cZcXKbaA7cT9cAID2lwbAefa03XaHy5Jti6uwuvDXfEps3doDf3XiLTSMBMhNaF4qXCDQIsMmRZ+svi19jAJXpJtLLW/PK2JjT2dywvuympBzI/V71r3dd/fxLjGSgPrUZ/JT9d6OVrQg0n8ThK5011/6MTe4OTlpPDw2V/zPJv/Xc6FB2TLYfAO1z31eSg0"}},{"csmcount":{"counter":"foresterPayloadSize","t":0,"value":931}}]}'

response = requests.post('https://fls-na.amazon.com/1/batch/1/OE/', cookies=cookies, headers=headers, data=data)
print(response.text) 