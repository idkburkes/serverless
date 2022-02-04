from http.server import BaseHTTPRequestHandler
from urllib import parse
import requests

class handler(BaseHTTPRequestHandler):

  def do_GET(self):
    url_path = self.path
    url_components = parse.urlsplit(url_path)
    query_string_list = parse.parse_qsl(url_components.query)
    map = dict(query_string_list)

    username = map['user']
    endpoint = f'https://leetcode.com/graphql/'
    # GraphQL query converted to JSON from https://leetcode.com/discuss/general-discussion/1297705/is-there-public-api-endpoints-available-for-leetcode
    query = f"{{ matchedUser(username: \"{username}\") {{ username submitStats: submitStatsGlobal {{ acSubmissionNum {{ difficulty count submissions }} }} }} }}"

    r = requests.post(endpoint, json={"query": query})
    leetcode_data = r.json()
    counts = leetcode_data['data']['matchedUser']['submitStats']['acSubmissionNum']

    resp = f'Leetcode solution submission data for {username}\n'
    if r.status_code == 200:
        for data in counts:
            difficulty = data['difficulty']
            completed = data['count']
            submissions = data['submissions']
            plural_c = 's' if int(completed) > 1 else ''
            plural_s = 's' if int(submissions) > 1 else ''
            resp += f'{difficulty}: {completed} solution{plural_c} accepted in {submissions} attempt{plural_s}\n'
    else:
        resp = f'API could not find Leetcode account \"{username}\"'
        print('error code: ',r.status_code)

    self.send_response(200)
    self.send_header('Content-type', 'text/plain')
    self.end_headers()
    self.wfile.write(resp.encode())
    return