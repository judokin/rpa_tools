import requests

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'ak-client-type': 'web',
    'ak-origin': 'https://erp.lingxing.com',
    'auth-token': '413784LivRRymhyRxZB3bStVsZyEqT+elwPSEPh6Uf/d0FTL7iHtb9KFmEDSl+ML/lIy2t59vASjJALuhONQSi17OjGzCCDPwH2ioaA1G4MyMlcAkQLDKqQF/KN2hWgQYY3mVCrn6SeN8pWNXVgK1A+ywl7o3TzJ+Jrl',
    'cache-control': 'no-cache',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://erp.lingxing.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://erp.lingxing.com/',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-storage-access': 'active',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'x-ak-company-id': '901161974801813504',
    'x-ak-env-key': 'SAAS-113',
    'x-ak-language': 'zh',
    'x-ak-platform': '1',
    'x-ak-request-id': '4a486709-6578-456d-9868-1280f69da287',
    'x-ak-request-source': 'erp',
    'x-ak-uid': '10727633',
    'x-ak-version': '3.5.4.3.0.115',
    'x-ak-zid': '213996',
}

json_data = {
    'start_date': '2025-01-22',
    'end_date': '2025-02-21',
    'store_ids': [],
    'marketplace_ids': [],
    'order_status': [
        'RECEIVED',
    ],
    'search_field': 'seller_fulfillment_order_id',
    'search_value': '',
    'multiple': 0,
    'is_hold': '1',
    'offset': 0,
    'length': 1000,
    'req_time_sequence': '/amzod/outbound/api/fbaOutboundOrder/page$$11',
}

response = requests.post('https://gw.lingxingerp.com/amzod/outbound/api/fbaOutboundOrder/page', headers=headers, json=json_data)
data = response.json()
for i,item in enumerate(data['data']['list']):
    print(i,item)
print(data)
import pdb;pdb.set_trace()
pass
# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"start_date":"2025-01-22","end_date":"2025-02-21","store_ids":[],"marketplace_ids":[],"order_status":["RECEIVED"],"search_field":"seller_fulfillment_order_id","search_value":"","multiple":0,"is_hold":"1","offset":0,"length":200,"req_time_sequence":"/amzod/outbound/api/fbaOutboundOrder/page$$11"}'
#response = requests.post('https://gw.lingxingerp.com/amzod/outbound/api/fbaOutboundOrder/page', headers=headers, data=data)