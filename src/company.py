from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .person import Person

from .helper.faker import faker
from .helper.moneyholder import Moneyholder, NotEnoughMoneyException
from .helper.logger import Logger

import random

class Company(Moneyholder):
    def __init__(self, logger: Logger):
        self.logger = logger
        self.name = faker.company()
        self.founded = faker.date_of_birth()
        self.money: float = random.random() * 10000
        self.num_products: int = 0
        self.employees: list[Person] = []
        self.logger.info(f"Company {self.name} founded on {self.founded}")
        
    def hire(self, person: Person, salary: float):
        self.employees.append(person)
        person.salary = salary
        person.company = self
        self.logger.info(f"Hired {person.name} with salary {salary}")
    
    def fire(self, person: Person):
        self.employees.remove(person)
        person.salary = 0.0
        person.company = None
        self.logger.info(f"{self.name} fired {person.name}")
    
    def sell(self):
        amount_sold = random.randint(0, self.num_products)
        self.num_products -= amount_sold
        self.gain_money(amount_sold * random.random() * 100)
    
    def update(self):
        self.pay_employees()
        self.sell()
    
    def pay_employees(self):
        for employee in self.employees:
            try:
                self.spend_money(employee.salary)
                employee.gain_money(employee.salary)
                self.logger.info(f"Paid {employee.name} salary {employee.salary}")
            except NotEnoughMoneyException as e:
                self.money = 0
                self.logger.error(f"Failed to pay {employee.name}: {e}")
                self.fire(employee)

    def __str__(self):
        return self.name