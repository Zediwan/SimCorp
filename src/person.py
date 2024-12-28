from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .company import Company

from .helper.moneyholder import Moneyholder
from .helper.faker import faker
from .helper.logger import Logger

import random
import math

class Person(Moneyholder):
    def __init__(self, logger: Logger):
        self.logger = logger
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
            # look for a job
            pass
        self.buy()

    def work(self):
        if self.company is None:
            raise Exception("Person has no company to work")
        
        # Produce goods
        produced_goods: int = math.floor(random.random() * self.proficency)
        self.company.num_products += produced_goods
        self.logger.info(f"{self.name} produced {produced_goods} goods")
        # Gain experience
        xp = produced_goods / (self.proficency * 10)
        self.proficency += xp
        self.logger.info(f"{self.name} gained {xp} experience")

    def buy(self):
        # Decide what to buy
        # Decide price to buy at
        # Try to buy
        pass

    def __str__(self):
        return self.name