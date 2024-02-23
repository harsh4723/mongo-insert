import json
import requests


def process_requests(input_file, output_file):
    # Read JSON array file containing request bodies
    with open(input_file, 'r') as f:
        requests_data = json.load(f)

    responses = []
    for request_data in requests_data:
        # Fire POST request with the request body
        url = f"http://34.86.235.188/sites/{request_data["sitekey"]}/products/_filter?query_tag={request_data["query_tag"]}"
        print("url",url )
        response = requests.post(url, json=request_data["query"])
        
        # Append response to list
        responses.append({
            "response": {
                "status_code": response.status_code,
                "text": response.text
            }
        })

    # Write responses to another JSON file
    with open(output_file, 'w') as f:
        json.dump(responses, f, indent=4)



input_file = "hodor_request_gcp_json_2.json"
output_file = "gcp_responses.json"
process_requests(input_file, output_file)