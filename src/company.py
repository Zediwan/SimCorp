from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .person import Person
    from .simulation import Simulation

from .helper.faker import faker
from .helper.moneyholder import Moneyholder, NotEnoughMoneyException
from .helper.logger import Logger

import random
import datetime

class Company(Moneyholder):
    CREATION_COST = 5000

    def __init__(self, logger: Logger, simulation: Simulation, money: float = None, founder: "Person" = None):
        self.logger = logger
        self.simulation = simulation

        if founder is not None:
            self.name = f"{founder.name} " + faker.company_suffix()
            self.founded = datetime.datetime.now()
            self.founder = founder
            self.dividend = random.random() * 0.1
        else:
            self.name = faker.company()
            self.founded = faker.date_of_birth()
            self.founder = None

        if money is not None:
            self.money = money
        else:
            self.money: float = random.random() * 10000

        self.num_products: int = 0

        self.employees: list[Person] = []

        self.logger.info(f"Company {self.name} founded on {self.founded}")
        
    def look_for_employee(self):
        # TODO: Decision making on who to consider hiring
        # TODO: Decision making on how much salary to offer
        if len(self.simulation.unemployed_people) > 0:
            target_person: Person = random.choice(self.simulation.unemployed_people)
            salary: float = random.random() * 5 * target_person.proficency
            self.hire(target_person, salary)

    def hire(self, person: Person, salary: float):
        # TODO: add decision process of the person to accept the job offer
        self.employees.append(person)
        person.join_company(self, salary)
        self.logger.info(f"Hired {person.name} with salary {salary}")
    
    def fire(self, person: Person, reason: str):
        self.employees.remove(person)
        person.leave_company()
        self.logger.info(f"Fired {person.name} because {reason}")
    
    def sell(self, amount: int = None):
        if amount is None:
            amount = random.randint(0, self.num_products)
        self.num_products -= amount
        self.gain_money(amount * random.random() * 10)
    
    def update(self):
        self.pay_founder()
        self.pay_employees()
        self.sell()
        self.look_for_employee()

        if self.money <= 0:
            self.declare_bankruptcy()

    def declare_bankruptcy(self):
        self.logger.info(f"Company {self.name} declared bankruptcy")
        self.simulation.remove_company(self)

        for employee in self.employees:
            self.fire(employee, "company declared bankruptcy")
    
    def pay_employees(self):
        for employee in self.employees:
            try:
                self.spend_money(employee.salary)
                employee.gain_money(employee.salary)
                #self.logger.info(f"Paid {employee.name} salary {employee.salary}")
            except NotEnoughMoneyException as e:
                self.logger.error(f"Failed to pay {employee.name}: {e}")
                self.sell_all_products()
                if self.money >= employee.salary:
                    self.spend_money(employee.salary)
                    employee.gain_money(employee.salary)
                    self.logger.info(f"Paid {employee.name} salary {employee.salary} after selling products")
                else:
                    self.money = 0
                    self.fire(employee, "the company does not have enough money to pay salary")

    def pay_founder(self):
        if self.founder is not None:
            dividend = self.money * self.dividend
            self.spend_money(dividend)
            self.founder.gain_money(dividend)
            self.logger.info(f"Paid {self.founder.name} {dividend} as dividend")

    def sell_all_products(self):
        self.logger.info(f"Company {self.name} is selling all products to generate money")
        self.sell(self.num_products)

    def __str__(self):
        return self.name