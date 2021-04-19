import jwt
import datetime

token=jwt.encode({'user':'Sunil', 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, 'hello')

try:
    data = jwt.decode(token, 'hello', algorithms='HS256')
except:
    print('error')

print('done')