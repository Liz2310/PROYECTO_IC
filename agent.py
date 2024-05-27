import ast
import numpy as np
import pandas as pd

class Agent:
    def __init__(self, 
               skill_percentage=None,
               number_employers=None,
               number_top_employers=None,
               education_level=None,
               top_school=None):
    
        self.skill_percentage = skill_percentage
        self.number_employers = number_employers
        self.number_top_employers = number_top_employers
        self.education_level = education_level
        self.top_school = top_school


    # Set percentage of skills desired in a candidate
    def set_skill_percentage(self):
        skills_level = int(input("""
Which level of skills are you looking for? (Enter corresponding number)

1 High (Very skilled)
2 Medium (Somewhat skilled)
3 Low (Basic skilled)
                                 
"""))

        if skills_level == 1:
            self.skill_percentage = 0.8

        elif skills_level == 2:
            self.skill_percentage = 0.5

        else:
            self.skill_percentage = 0.1
        
    
    # Set number of past employers desired in a candidate
    def set_employer_count(self):
        employer_count_level = int(input("""
How many past employers are you looking for? (Enter corresponding number)

1 High (Very experienced)
2 Medium (Somewhat experienced)
3 Low (Basic experienced)
                                 
"""))

        if employer_count_level == 1:
            self.number_employers = (4, 1000) # 1000 represents a value of 4+

        elif employer_count_level == 2:
            self.number_employers = (2, 4)

        else:
            self.number_employers = (0,2)
        

    # Set number of past employers that are considered to be
    # top companies desired in a candidate
    def set_top_employer_count(self):
        top_employer_count_level = int(input("""
How many top employers are you looking for? (Enter corresponding number)

1 High (At least 2)
2 Medium (At least 1)
3 Low (None)
                                 
"""))

        if top_employer_count_level == 1:
            self.number_top_employers = 2

        elif top_employer_count_level == 2:
            self.number_top_employers = 1

        else:
            self.number_top_employers = 0        


    # Set level education desired in a candidate
    def set_education_level(self):
        qualification_level = int(input("""
What level of education are you looking for? (Enter corresponding number)

1 High (At least a master's)
2 Medium (At least university/college degree)
3 Low (High school)
                                 
"""))

        if qualification_level == 1:
            self.education_level = "m.s"
            
        elif qualification_level == 2:
            self.education_level = "b.s"

        else:
            self.education_level = "none"
        

    # Set if candidate is to come from what is considered
    # to be top schools 
    def set_top_education(self):
        top_education = int(input("""
How many top schools are you looking for? (Enter corresponding number)

1 High (At least 2)
2 Medium (At least 1)
3 Low (None)
                                 
"""))

        if top_education == 1:
            self.top_school = 2

        elif top_education == 2:
            self.top_school = 1

        else:
            self.top_school = 0


    # Get percentage of skills desired in a candidate
    def get_skill_percent(self, dataframe, skill_bank):
        total_skill_bank = len(skill_bank)
        skill_percentages = []

        for index, row in dataframe.iterrows():
            skill_set = row["skills"]

            skill_set = set(ast.literal_eval(skill_set))
            skill_bank = set(skill_bank)

            common_skills = (skill_set & skill_bank)
            percentage = ((100 * len(common_skills)) / total_skill_bank) / 100

            if percentage < self.skill_percentage:
                dataframe.drop(index, inplace=True)
            else:
                skill_percentages.append(percentage)
        
        dataframe["skill_percentages"] = skill_percentages

        return dataframe


    # Get count of past employers
    def get_employer_count(self, dataframe):
        employer_count = []

        for ind in dataframe.index:
            candidate_companies = dataframe["companies"][ind]
            candidate_companies = ast.literal_eval(candidate_companies)


            candidate_company_count = 0
            for company in candidate_companies:
                candidate_company_count += 1

            if candidate_company_count >= self.number_employers[0] and candidate_company_count <= self.number_employers[1]:
                employer_count.append(candidate_company_count)
            else:
                dataframe.drop(ind, inplace=True)

        dataframe["employer_count"] = employer_count

        return dataframe


    # Get count of any past employers that are considered 
    # to be top companies
    def get_top_companies(self, dataframe, top_companies_bank):
        top_company_count = []

        for ind in dataframe.index:
            candidate_companies = dataframe["companies"][ind]
            candidate_companies = ast.literal_eval(candidate_companies)

            candidate_companies_set = set(candidate_companies)
            companies_bank_set = set(top_companies_bank)

            common_companies = (candidate_companies_set & companies_bank_set)

            if len(common_companies) >= self.number_top_employers:
                top_company_count.append(len(common_companies))
            else:
                dataframe.drop(ind, inplace=True)
        
        dataframe["top_company_count"] = top_company_count

        return dataframe
    

    # Get count of all degrees in the desired areas for 
    # a given candidate
    def get_education_level(self, dataframe, areas):
        education_level = []

        for ind in dataframe.index:
            candidate_degrees = dataframe["degree"][ind]
            candidate_degrees = ast.literal_eval(candidate_degrees)

            for degree in candidate_degrees:
                if self.education_level in degree:
                    continue
                else:
                    dataframe.drop(ind, inplace=True)
            
        
        for ind in dataframe.index:
            candidate_degrees = dataframe["degree"][ind]
            candidate_degrees = ast.literal_eval(candidate_degrees)

            area_count = 0
            for degree in candidate_degrees:
                for area in areas:
                    if area in degree:
                        area_count += 1

            if self.education_level == "none":
                education_level.append(0)
                continue
            
            if area_count == 0:
                dataframe.drop(ind, inplace=True)
            else:
                education_level.append(area_count)
            
        dataframe["education_level"] = education_level

        return dataframe
    

    # Get count of what are considered to be
    # top schools for a given candidate
    def get_top_schools(self, dataframe, top_schools):
        top_school_count = []

        for ind in dataframe.index:
            candidate_schools = dataframe["school"][ind]
            candidate_schools = ast.literal_eval(candidate_schools)

            candidate_schools_set = set(candidate_schools)
            schools_bank_set = set(top_schools)

            common_schools = (candidate_schools_set & schools_bank_set)
            
            if len(common_schools) >= self.top_school:
                top_school_count.append(len(common_schools))
            else:
                dataframe.drop(ind, inplace=True)
        
        dataframe["top_school_count"] = top_school_count
                
        return dataframe
            
