import re

class ValidateSchema:
    @staticmethod
    def validate_password_length(pass_:str):
        special_characters = set("-@#$%^&+=")
        if len(pass_) <= 7:
            raise ValueError("Password must contains 8 characters")
        if bool(re.match(r'^[A-Z]', pass_)) == False:
            raise ValueError("Password must start with capital letter")
        if not any(c in special_characters for c in pass_):
            raise ValueError("Password must include at least one special character like '@', '#', etc.")
        if not any(char.isdigit() for char in pass_):
            raise ValueError("Password must contain at least one digit")
        return pass_
    
    @staticmethod
    def validate_balance(bal:int):
        if bal <= 0:
            raise ValueError("Balance must be more than zero")
        return bal
    
    @staticmethod
    def name_no_specials(val: str):
        if not val.replace(" ", "").isalpha():
            raise ValueError("El nombre solo debe contener letras")
        return val