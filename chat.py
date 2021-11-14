import requests
import re
import json

s = requests.session()
def login(user, passw):
    global stoken
    r = s.get("https://bs.to").text
    stoken = re.search('name="security_token" value=.*type="submit" value="Login"', r.replace("\n", "")).group().replace(" ", "").replace("\t", "").replace('name="security_token"value="', "").replace('"/><inputtype="submit"value="Login"', "")
    r = s.post("https://bs.to", {"login[user]":user, "login[pass]":passw, "security_token":stoken}).text
    stoken = re.search('<meta name="security_token" content=".*<meta name="description" content=', r.replace("\n", "")).group().replace(" ", "").replace("\t", "").replace('<metaname="security_token"content="', "").replace('<metaname="description"content=', "").replace('"/>', "")


lastmsg = "0"
def sendmsg(msg):
    r = s.post("https://bs.to/ajax/sb-send.php", {"token":stoken, "last":lastmsg, "text":msg})
    return(str(r))

def getmsgs():
    global lastmsg
    r = json.loads(s.post("https://bs.to/ajax/sb-posts.php", {"token":stoken, "last":lastmsg}).text)
    k = []
    if(r["posts"]!=[]):
        lastmsg = r["posts"][0]["id"]
        for a in r["posts"]:
            k = [a] + k
    return(k)
