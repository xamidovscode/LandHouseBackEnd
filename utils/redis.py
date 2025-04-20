import json
import redis


class Redis:
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

    @classmethod
    def save(cls, phone, full_name, role, code, device_token, expire_time):
        key = phone
        value = {
            'phone': phone,
            'full_name': full_name,
            'role': role,
            'code': code,
            'device_token': device_token,
        }
        value_json = json.dumps(value)
        return cls.redis_client.setex(key, expire_time, value_json)

    @classmethod
    def get(cls, key):
        value_json = cls.redis_client.get(key)
        if value_json:
            decoded_value = value_json.decode('utf-8')
            value_dict = json.loads(decoded_value)
            return key, value_dict
        return key, None
