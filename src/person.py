from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .simulation import Simulation

from .company import Company

from .helper.moneyholder import Moneyholder
from .helper.faker import faker
from .helper.logger import Logger

import random
import math

class Person(Moneyholder):
    def __init__(self, logger: Logger, simulation: Simulation):
        self.logger = logger
        self.simulation = simulation
        self.name = faker.name()
        self.birthday = faker.date_of_birth()
        self.money: float = 0.0
        self.salary: float = 0.0
        self.company: "Company" = None
        self.proficency: float = random.random() * 10
        self.logger.info(f"Person {self.name} born on {self.birthday}")

    def update(self):
        if self.company:
            self.work()
        else:
            self.look_for_job_or_found_company()
        self.buy()

    def work(self):
        if self.company is None:
            raise Exception("Person has no company to work")
        
        # Produce goods
        produced_goods: int = math.floor(random.random() * self.proficency)

        self.company.num_products += produced_goods
        # Gain experience
        xp = (produced_goods + 1) / (self.proficency * 10)
        self.proficency += xp

    def look_for_job_or_found_company(self):
        if (self.money >= (Company.CREATION_COST * 2)) and random.random() < 0.01:  # Threshold to found a company
            self.found_company()
        else:
            # Logic to look for a job
            pass

    def found_company(self):
        self.spend_money(Company.CREATION_COST)
        starting_funds: float = random.randint(0, math.floor(self.money))
        self.spend_money(starting_funds)

        new_company = Company(logger=self.logger, simulation=self.simulation, money=starting_funds, founder=self)
        self.simulation.add_company(new_company)

        self.logger.info(f"{self.name} founded a new company {new_company.name}")

    def join_company(self, company: Company, salary: float):
        self.company = company
        self.salary = salary
        self.simulation.unemployed_people.remove(self)

    def leave_company(self):
        self.company = None
        self.salary = 0.0
        self.simulation.unemployed_people.append(self)

    def buy(self):
        # Decide what to buy
        # Decide price to buy at
        # Try to buy
        pass

    def __str__(self):
        return self.name