from elasticsearch import Elasticsearch
import json

HOST = 'localhost'
PORT = 9200
SPECIFIC_FIELDS = True

class Search:
    def __init__(self):
        self.es = Elasticsearch("http://localhost:9200")
    def index_data(self, index_name, id, body):
        res = self.es.index(index=index_name, id=id, body=body)
        return res
    def search(self, index_name, body):
        res = self.es.search(index=index_name, body=body)
        return res
    def more_like_this(self, input_string, spcific_fields=True):
        if spcific_fields:
            fields = ["title", "first_page_summary","geners"]
        else:
            fields = ["summaries", "synopsises"]
        query = {
                "_source": fields,
                "query": {
                    "more_like_this" : {
                    "fields" : fields,
                    "like" : input_string,
                    "min_term_freq" : 0
                    }
                },
                "size": 15
            }
        return query
    def indent(self, res):
        return json.dumps(res, indent=4)

    def run(self):
        while(True):
            string_input = input("Press Enter your command: \n 1. Index Data \n 2. Search Data \n 3. Exit \n")
            if string_input == '1':
                with open('data.json') as f:
                    data = json.load(f)
                    index_name = 'imdb_movies'
                    for i in range(len(data)):
                        res = self.index_data(index_name, data[i]["id"], data[i])
                        print(res)
            elif string_input == '2':
                input_string = input("Enter the search query: ")
                query = self.more_like_this(input_string, SPECIFIC_FIELDS)
                res = self.search('imdb_movies', query)
                res = self.indent(res)
                print(res)
                with open('output.txt', 'w') as f:
                    f.write("Search Query: " + input_string + "\n")
                    f.write(res)
                
                
            elif string_input == '3':
                break

if __name__ == '__main__':
    search = Search()
    search.run()
