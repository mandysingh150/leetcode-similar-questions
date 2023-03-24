"""
    Contains utility function to update upto which the problems has been downloaded, writing chapter info to a file, resetting configuration,
    reading upto which the problems has been downloaded
"""
import pickle

def update_tracker(file_name, problem_num):
     """

     """
     with open(file_name, "w") as f:
         f.write(str(problem_num))

def reset_configuration():
    """
        Resets problem num downloaded upto to -1
        Resets csv file
    """
    update_tracker("track.conf", -1)

    with open("data.csv", "w") as f:
        f.write('frontend_question_id,question_title,problem_statement_examples_contraints,solution_page_link,solution_content\n')


def read_tracker(file_name):
    """
    
    """
    with open(file_name, "r") as f:
        return int(f.readline())




