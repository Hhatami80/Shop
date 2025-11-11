from abc import ABC, abstractmethod
import random
import requests
from django.conf import settings


class BaseSmsManager(ABC):

    @abstractmethod
    def send_sms(self, receiver_phone: str, message: str) -> bool:
        """ send sms, return True if successful, o.w. False """
        pass


class KavehNegarSmsManager(BaseSmsManager):

    def __init__(self):
        self.api_key = settings.PROVIDER_API_KEY

    def send_sms(self, receiver_phone: str, message: str) -> bool:
        url = f"https://api.kavenegar.com/v1/{self.api_key}/sms/send.json"
        payload = {
            'receptor': receiver_phone,
            'message': message
        }
        response = requests.post(url, data=payload)
        return response.status_code == 200


class GhasedakSMSProvider(BaseSmsManager):
    def __init__(self):
        self.api_key = settings.PROVIDER_API_KEY

    def send_sms(self, phone_number: str, message: str) -> bool:
        headers = {'apikey': self.api_key, "cache-control": "no-cache",
                   "content-type": "application/x-www-form-urlencoded"}
        payload = {'message': message, 'receptor': phone_number, 'linenumber': '1000XXX'}
        response = requests.post('https://api.ghasedak.me/v2/sms/send/simple', data=payload, headers=headers)
        return response.status_code == 200


class ConsoleSMSProvider(BaseSmsManager):
    def send_sms(self, receiver_phone: str, message: str) -> bool:
        print(f"Sent SMS to {receiver_phone} with this content : {message}")
        return True

def get_sms_provider():
    provider_options = ["kavehnegar", "ghasedak", "console"]
    provider = settings.PROVIDER
    if provider == 'kavehnegar':
        return KavehNegarSmsManager()
    elif provider == 'ghasedak':
        return GhasedakSMSProvider()
    elif provider == 'console':
        return ConsoleSMSProvider()
    else:
        return


class OTPService:
    def __init__(self):
        self.sms_provider = get_sms_provider()

    def send_otp(self, phone_number: str, otp_code: str) -> str:
        otp = otp_code if otp_code else str(random.randint(100000, 999999))
        message = f" مشتری گرامی کد شما:{otp} "
        success = self.sms_provider.send_sms(phone_number, message)
        if not success:
            raise Exception("Failed to send OTP")
        return otp
