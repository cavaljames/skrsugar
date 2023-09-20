"""
@File    :   unit_test.py    
@Contact :   zhangyu@onesight.com

@Modify Time    @Author @Version    @Description
------------    ------- --------    -----------
2023/9/18      zhangyu 1.0         None
"""


def compair_cookie(cookie1, cookie2):
    cookie1s, cookie2s = cookie1.split(';'), cookie2.split(';')
    ck1map, ck2map = {}, {}
    for ck1entry in cookie1s:
        k, v = tuple(ck1entry.split('='))
        ck1map.update({k.strip(): v.strip()})
    for ck2entry in cookie2s:
        k, v = tuple(ck2entry.split('='))
        ck2map.update({k.strip(): v.strip()})
    ck1tuple = sorted(ck1map.items(), key=lambda x: x[0])
    ck2tuple = sorted(ck2map.items(), key=lambda x: x[0])
    ck1str = '; '.join(['='.join([k, v]) for k, v in ck1tuple])
    ck2str = '; '.join(['='.join([k, v]) for k, v in ck2tuple])
    print(ck1str)
    print(ck2str)
    return ck1str, ck2str


if __name__ == '__main__':
    from skrbt.skrmain import get_refresh_cookie
    get_refresh_cookie()

