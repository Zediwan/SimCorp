from __future__ import annotations

from .company import Company
from .person import Person
from .helper.logger import Logger

import random

class Simulation:
    num_starting_companies: int = 20
    num_starting_people: int = 100

    def __init__(self, logger: Logger = None):
        self.logger = logger if logger else Logger(__name__)
        self.companies: list[Company] = []
        self.people: list[Person] = []

        self.logger.info("Initializing simulation")

        for _ in range(Simulation.num_starting_companies):
            self.companies.append(Company(logger=self.logger))

        for _ in range(Simulation.num_starting_people):
            self.people.append(Person(logger=self.logger))

        self.logger.info("Simulation initialized")

    def run(self):
        for company in self.companies:
            if company.money <= 0:
                for employee in company.employees:
                    employee.company = None
                    employee.salary = 0.0
                self.companies.remove(company)
                self.logger.info(f"Company {company.name} went bankrupt")
                continue
            
            if random.random() < 0.1:
                unemployed_people = [person for person in self.people if person.company is None]
                if len(unemployed_people) > 0:
                    company.hire(random.choice(unemployed_people), random.random() * 1000)
        
        for person in self.people:
            person.update()