import json
import pandas as pd
from agent import Agent
from skcriteria import Data, MIN, MAX
from skcriteria.madm import simple
from sklearn.preprocessing import minmax_scale


def decision_tree(dataframe, 
                  skills, 
                  top_employers, 
                  areas,
                  top_schools):
    
    agent = Agent()


    # SKILLS AND ABILITIES
    agent.set_skill_percentage()
    pruned_skills_dataframe = agent.get_skill_percent(dataframe, skills)

    # EXPERIENCE
    # How many employers have they had previous to this one?
    agent.set_employer_count()
    pruned_employer_count_dataframe = agent.get_employer_count(pruned_skills_dataframe)

    # Which type of employers
    agent.set_top_employer_count()
    top_company_dataframe = agent.get_top_companies(pruned_employer_count_dataframe, top_employers)
    
    # QUALIFICATIONS
    # What’s their level of education?
    agent.set_education_level()
    education_dataframe = agent.get_education_level(top_company_dataframe, areas)

    # Did they go to what we classify as a top-tier school?
    agent.set_top_education()
    top_school_dataframe = agent.get_top_schools(education_dataframe, top_schools)

    criteria_df = top_school_dataframe[["id", 
                                        "skill_percentages", 
                                        "employer_count",
                                        "top_company_count", 
                                        "education_level", 
                                        "top_school_count"]]
    
    if criteria_df.empty:
        print("No candidates meet the criteria")
        return
        
    # Normalize data using minmax scale that converts
     # features into the range [-1, 1]
    df = criteria_df.iloc[:, 1:].values.copy()
    normalized_data = minmax_scale(df, (-1, 1))


    # Create Data object to apply decision maker on
    criteria_data = Data(
            normalized_data,
            [MAX, MAX, MIN, MIN, MIN], # direction of goodness for each column
            anames = criteria_df["id"],
            cnames = criteria_df.columns[1:]
    )

    # Apply simple WeightedSum decision maker
    decision_maker = simple.WeightedSum()
    ranking = decision_maker.decide(criteria_data)

    print(ranking)

try:

    input_resumes = "./resumes_copy.csv"
    input_resumes = pd.read_csv(input_resumes)

    input_position = open("./positions/entry_position.json")
    input_position = json.load(input_position)

    # input_position = open("./positions/trainee_position.json")
    # input_position = json.load(input_position)

    print(input_position["title"])
    print()

    # get into from position
    skills = input_position["skills"]
    top_employers = input_position["experience"]["top employers"]
    areas = input_position["qualifications"]["areas"]
    top_schools = input_position["qualifications"]["top school"]
    
    decision_tree(input_resumes,
                  skills,
                  top_employers,
                  areas,
                  top_schools)

except Exception as e:
    print(e)




