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
        self.logger.info(f"Fired {person.name}")
    
    def sell(self):
        pass
    
    def update(self):
        self.pay_employees()
    
    def pay_employees(self):
        for employee in self.employees:
            try:
                self.spend_money(employee.salary)
                employee.gain_money(employee.salary)
                self.logger.info(f"Paid {employee.name} salary {employee.salary}")
            except NotEnoughMoneyException as e:
                self.logger.error(f"Failed to pay {employee.name}: {e}")
                self.fire(employee)