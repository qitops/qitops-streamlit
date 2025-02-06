import json
import pandas as pd
from typing import Dict, Union, List

def load_json_data(file_path: str) -> Dict:
    """Load JSON data from file or uploaded content"""
    with open(file_path) as f:
        return json.load(f)

def parse_qa_data(data: Dict) -> pd.DataFrame:
    """Process test case data from test_cases.json structure"""
    tickets = []
    for ticket in data['tickets']:
        for test_case in ticket['test_cases']:
            tickets.append({
                'ticket_key': ticket['key'],
                'summary': ticket['summary'],
                'type': ticket['type'],
                'ticket_priority': ticket['priority'],
                'test_case_id': test_case['id'],
                'description': test_case['description'],
                'category': test_case['category'],
                'test_case_priority': test_case['priority']
            })
    return pd.DataFrame(tickets)

def parse_performance_data(data: Dict) -> pd.DataFrame:
    """Process performance data from performance_test_results.json"""
    requests = []
    for req in data['requests']:
        record = {
            'endpoint': req['endpoint'],
            'method': req['method'],
            'total_requests': req['total_requests'],
            'success_rate': req['success_count'] / req['total_requests'],
            'error_rate': req['error_count'] / req['total_requests'],
            'avg_response_ms': req['average_response_time_ms'],
            'throughput_rps': req['throughput_rps']
        }
        # Add percentiles
        record.update({f'p{k[:-2]}': v for k, v in req['percentiles'].items()})
        requests.append(record)
    
    return pd.DataFrame(requests)

def detect_data_type(data: Dict) -> str:
    """Identify JSON data type based on structure"""
    if 'tickets' in data:
        return 'test_cases'
    elif 'test_metadata' in data:
        return 'performance'
    return 'unknown'

def json_to_documents(data: Dict) -> List[Dict]:
    """Convert JSON data to text documents for embedding"""
    documents = []
    
    if 'tickets' in data:
        for ticket in data['tickets']:
            for test_case in ticket['test_cases']:
                doc = {
                    'type': 'test_case',
                    'content': f"Test case {test_case['id']}: {test_case['description']}",
                    'metadata': {
                        'ticket': ticket['key'],
                        'category': test_case['category'],
                        'priority': test_case['priority']
                    }
                }
                documents.append(doc)
    
    if 'requests' in data:
        for request in data['requests']:
            doc = {
                'type': 'performance_test',
                'content': f"Performance test on {request['endpoint']} ({request['method']})",
                'metadata': {
                    'endpoint': request['endpoint'],
                    'success_rate': request['success_count']/request['total_requests'],
                    'avg_response': request['average_response_time_ms']
                }
            }
            documents.append(doc)
    
    return documents 