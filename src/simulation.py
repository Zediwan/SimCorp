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
        self.bankrupt_companies: list[Company] = []
        self.new_companies: list[Company] = []

        self.unemployed_people: list[Person] = []
        self.people: list[Person] = []

        self.logger.info("Initializing simulation")

        for _ in range(Simulation.num_starting_companies):
            self.companies.append(Company(logger=self.logger, simulation=self))

        for _ in range(Simulation.num_starting_people):
            person = Person(logger=self.logger, simulation=self)
            self.people.append(person)
            self.unemployed_people.append(person)

        self.logger.info("Simulation initialized")

    def run(self):
        for company in self.companies:
            company.update()
        
        for person in self.people:
            person.update()

        if random.random() < 0.01:
            person = Person(logger=self.logger, simulation=self)
            self.people.append(person)
            self.unemployed_people.append(person)

    def add_company(self, company: Company):
        self.new_companies.append(company)
        self.companies.append(company)
        self.logger.info(f"New company {company.name} added")

    def remove_company(self, company: Company):
        self.companies.remove(company)
        self.bankrupt_companies.append(company)
        self.logger.info(f"Company {company.name} removed")