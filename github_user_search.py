#/usr/bin/python

import requests
import argparse
import time

def main(user,passwd,count):
    # Main code which retrieves data.
    # Hardcoding the base url 
    github_api_url='https://api.github.com/search/users?q=location:singapore&per_page=20'

    total_users = 0
    #params = 'q=location:pune&per_page=20'

    current_session=requests.Session()

    try :  #Handling connection and timeout exceptions raised with requests.get
    
        while github_api_url is not None:
            # TODO handle timeout
            
            response_data=current_session.get(url=github_api_url,auth=(user,passwd)) # (params=params))
            
            status_code = response_data.status_code
            
            # Only looking at successful codes (data found or no data found, ignoring other codes and incomplete results for now)
            if status_code in (200,204):
                total_users +=  print_data(response_data.json())
                if (total_users >= count) :  break
                github_api_url = parse_link_headers(response_data)
            elif status_code == 403: #Rate limit hit TODO, Dont incur an api-hit with rate limit violaton
                pause_till(response_data['X-RateLimit-Reset'])
            else: 
            # Other responses with get request , not handled for now
                github_api_url = None

    except requests.exceptions.RequestException as e: 
        print "Program ended due to Connection error details : " + str(e)

# Extract login user name only (for now) from list of retrieved users
def print_data(response_json):
    # users is list of dict object ,  :t user_list :: [dict]
    user_list = response_json['items']
    for i in user_list:
        print i['login']
    return len(user_list) 

#Extract link info for pagination from headers. Return 'None' is none exists
def parse_link_headers(response):
    links = response.links
    # on first page and no next links OR no data found
    if links == {} :
       return None
    else:
       next_link = links.get('next',None)
       # on last page after navigating
       if next_link is None :
           return None
       else: # next page exists
           return next_link['url']

#Pause code and wait for rate window to reset
def pause_till(reset_sec):
    current_time = time.time()
    if current_time < reset_sec : sleep(reset_sec - current_time) 
    
            
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("user")
    parser.add_argument("passwd")
    parser.add_argument("count",type=int)
    args = parser.parse_args()
    # Call main with authorization and no of users to retrieve
    main(args.user,args.passwd,args.count)
