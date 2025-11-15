def send_otp(self, phone_number: str, otp_code: str) -> str:
    message = f" مشتری گرامی کد شما: {otp_code} "
    # below line is for dev env, please remove it in production
    print(f"Sending OTP to {phone_number}: {message}")
    return otp_code
