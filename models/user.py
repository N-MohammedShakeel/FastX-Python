class User:
    def __init__(self, user_id, name, email, password, role, wallet=0.00):
        self.__id = user_id
        self.__name = name
        self.__email = email
        self.__password = password
        self.__role = role
        self.__wallet = float(wallet)

    @property
    def id(self): 
        return self.__id
    
    @property
    def name(self): 
        return self.__name
    
    @property
    def email(self): 
        return self.__email
    
    @property
    def password(self): 
        return self.__password
    
    @property
    def role(self): 
        return self.__role
    
    @property
    def wallet(self): 
        return self.__wallet

    def deposit_money(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.__wallet += amount

    def deduct_money(self, amount):
        if amount <= 0:
            raise ValueError("Deduction amount must be positive.")
        if self.__wallet < amount:
            raise ValueError("Insufficient balance.")
        self.__wallet -= amount