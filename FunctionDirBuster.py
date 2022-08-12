import logging
import urllib.request
import azure.functions as func



def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    #Pull the wordlist from github
    url = 'https://raw.githubusercontent.com/cno-io/bh_shared/master/lists/quickhits_noslash_short.txt'
    resp = urllib.request.urlopen(url)
    #split the wordlist for iterations
    wordlist = resp.read().decode('utf-8').splitlines()
    
    #initialize an empty return list
    ret = []
    
    #attempt to retrieve the target through various possible methods
    target = req.params.get('target')
    if not target:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            target = req_body.get('target')

    if target:
        logging.info('Set target as ' + target)
        #iterate through the wordlist and return the HTTP response code
        for i in wordlist:
            url = target + i
            try:
                resp = urllib.request.urlopen(url)
                ret.append((resp.code, url))
            except urllib.error.HTTPError as error:
                ret.append((error.code, url))
                pass

        return func.HttpResponse("This HTTP triggered function executed successfully.\n" + '\n'.join(map(str, ret)))
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully but no target was supplied. Pass a target in the query string or in the request body.",
             status_code=200
        )