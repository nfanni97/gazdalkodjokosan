from logging import Logger
from textwrap import dedent
from typing import Self

import constants
from utils import format_int

class Player:
    def __init__(self, name: str, l: Logger) -> None:
        # TODO: insurance class
        # TODO: loan class
        self.name = name
        self.logger = l.getChild(self.name)
        self.car_payments = 0
        self.house_payments = 0
        self.balance = 3000000
        self.car_insurance = False
        self.house_insurance = False
        
    @property
    def has_car_loan(self) -> bool:
        return self.car_payments > 0
    
    @property
    def is_car_paid_for(self) -> bool:
        return self.car_payments == constants.Car.LOAN
    
    @property
    def has_house_loan(self) -> bool:
        return self.house_payments > 0
    
    @property
    def is_house_paid_for(self) -> bool:
        return self.house_payments == constants.House.LOAN
    
    def add_balance(self, amount: int) -> None:
        self.balance += amount
        self.logger.info(f'Adding to balance: {format_int(amount)}, new balance is {format_int(self.balance)}')
        
    def check_balance(self, amount: int) -> None:
        if self.balance < amount:
            raise Exception(f'Cannot pay {format_int(amount)}, when balance is only {format_int(self.balance)}')
        
    def pay_for_car(self, amount: int) -> None:
        self.check_balance(amount)
        if self.car_payments + amount > constants.Car.LOAN:
            original_amount = amount
            amount = constants.Car.LOAN-self.car_payments
            self.logger.warning(f'{format_int(original_amount)} would be too much to pay towards car, only adding {format_int(amount)}')
        self.car_payments += amount
        self.balance -= amount
        self.logger.info(f'After paying {format_int(amount)} towards car, only {format_int(constants.Car.LOAN-self.car_payments)} to go.')
        
    def pay_for_house(self, amount: int) -> None:
        self.check_balance(amount)
        if self.house_payments + amount > constants.House.LOAN:
            original_amount = amount
            amount = constants.House.LOAN-self.house_payments
            self.logger.warning(f'{format_int(original_amount)} would be too much to pay towards house, only adding {format_int(amount)}')
        self.house_payments += amount
        self.balance -= amount
        self.logger.info(f'After paying {format_int(amount)} towards house, only {format_int(constants.House.LOAN-self.house_payments)} to go.')
    
    def get_car_insurance(self) -> None:
        self.logger.info('Getting car insurance')
        self.pay_car_insurance()
        
    def get_house_insurance(self) -> None:
        self.logger.info('Getting house insurance')
        self.pay_house_insurance()
        
    def pay_car_insurance(self) -> None:
        if self.car_insurance:
            amount = constants.Car.INSURANCE
            self.check_balance(amount)
            self.logger.info('Paying car insurance')
            self.add_balance(-amount)
        
    def pay_house_insurance(self) -> None:
        if self.house_insurance:
            amount = constants.House.INSURANCE
            self.check_balance(amount)
            self.logger.info('Paying house insurance')
            self.add_balance(-amount)
        
    def go_through_start_automatic(self, amount: int = 500000) -> None:
        self.logger.info('Performing automatic part of start-of-round steps')
        self.add_balance(amount)
        self.pay_car_insurance()
        self.pay_house_insurance()
        
    def step_on_start_automatic(self) -> None:
        self.go_through_start_automatic(1000000)
        
    def pay_interest(self) -> None:
        self.balance = int(self.balance*1.07)
        self.logger.info(f'New balance is {format_int(self.balance)}')
    
    def serialize(self) -> str:
        return f'{self.name}: {self.car_payments},{self.house_payments},{self.balance}: {self.car_insurance},{self.house_insurance}'
    
    @classmethod
    def deserialize(cls, ser: str, l: Logger) -> Self:
        name, money, insurance = ser.split(': ')
        car,house,balance = list(map(int,money.split(',')))
        car_ins, house_ins = list(map(bool,insurance.split(',')))
        p = cls(name, l)
        p.car_payments = car
        p.house_payments = house
        p.balance = balance
        p.car_insurance = car_ins
        p.house_insurance = house_ins
        return p
    
    def print(self) -> str:
        return dedent(f'''
                      {self.name}
                      Car loan: {format_int(self.car_payments)} ({'insurance' if self.car_insurance else 'no insurance'})
                      House loan: {format_int(self.house_payments)} ({'insurance' if self.house_insurance else 'no insurance'})
                      Balance: {format_int(self.balance)}''')[1:]
        