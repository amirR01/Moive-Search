import numpy as np
import pandas as pd
import json

def average_precision(actual,predicted):
    score = 0.0
    num_hits = 0.0
    magic_number = 10
    for i, p in enumerate(predicted[0:min(len(predicted),magic_number)]):
        if p in actual and p not in predicted[:i]:
            num_hits += 1.0
            score += num_hits / (i + 1.0)
    
    return score / magic_number

def mean_average_precision(actual_list,predicted_list):
    return np.mean([average_precision(a,p) for a,p in zip(actual_list,predicted_list)])

def reciprocal_rank(actual,predicted):
    score = 0.0
    magic_number = 10

    for i,p in enumerate(actual):
        if p in predicted[0:min(len(predicted),magic_number)]:
            score += 1.0/(i+1)
        
    return score / magic_number

def mean_reciprocal_rank(actual_list,predicted_list):
    return np.mean([reciprocal_rank(a,p) for a,p in zip(actual_list,predicted_list)])


def get_ids_from_elasticsearch_response(response):
    ids = []
    for hit in response['hits']['hits']:
        ids.append(hit['_id'])
    return ids

def get_ids_from_user_input(response):
    try:
        ids_and_scores = eval(response)
    except:
        ids_and_scores = []
    ids = []
    for id,score in ids_and_scores:
        ids.append(id)
    return ids

def read_elasticsearch_response_from_file(file_path):
    with open(file_path) as f:
        responses = json.load(f)
    return responses

def read_user_responses_from_csv_file(file_path):
    df = pd.read_csv(file_path)
    return df

def save_results_to_csv_file(df,file_path):
    df.to_csv(file_path)



def main():
    user_responses = read_user_responses_from_csv_file('Phase 1 Scores - Sheet1.csv')
    elasticsearch_responses = read_elasticsearch_response_from_file('./results/Heists_and_robberies.json')
    
    user_responses['ids'] = user_responses['Search Results query-3'].apply(get_ids_from_user_input)
    print(user_responses)
    elasticsearch_response = get_ids_from_elasticsearch_response(elasticsearch_responses)
    
    for i in range(len(user_responses)):
        ap = average_precision(user_responses['ids'][i],elasticsearch_response)
        rr = reciprocal_rank(user_responses['ids'][i],elasticsearch_response)
        string_to_save = "AP: " + str(round(ap,2)) + " RR: " + str(round(rr,2))
        user_responses.loc[i,'Scores'] = string_to_save
        save_results_to_csv_file(user_responses,'Phase 1 Scores - Sheet1.csv')
        

if __name__ == '__main__':
    main()
