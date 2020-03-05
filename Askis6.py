# Author : Χρήστος Κωνσταντινίδης
# Κωδικός: ΜΠΛ19029

from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from datetime import datetime, date, time, timedelta
import re

NUM_OF_USERS = 2
NUM_OF_TWEETS = 50

# Εγκατάσταση του tweepy μέσα από την python
#   *** python -m pip install tweepy ***
#       python -m pip install package_name
#       python -m pip install --upgrade pip ή package_name

#Συνάρτηση βασικού τριμαρίσματος κειμένου
def basicTextTrimming(alist):
    # Συνάρτηση για την διαγραφή τεριμένων περιπτώσεων άρθρα, URL, κτλ....
    b = alist
    b = re.sub('[.!,]*', "", b)
    b = re.sub('([Hh]e )|([Ss]he )|([Ii]t )|([Yy]ou )|([Yy]ou are)|(I )|([Ww]ill )|([Hh]ave )|([Hh]ad )|([Bb]een )', "",
               b)
    b = re.sub('([#]+[A-Za-z0-9]+)*|(@[A-Za-z0-9]+)*|((http|https)://[A-Za-z0-9.]+/[A-Za-z0-9.]+)+', "", b)
    b = re.sub('([Ii]s )|([Hh]i[sm] )|(\n)|([Tt]he )|(a )|(to )|([Hh]e )|([Ss]he )', "", b)
    b = re.sub('([fF]or )|([Oo]f[, ])|(was[, ])|(be[, ])|(and )', "", b)
    b = re.sub('([Oo][Uu][Tt])|([Gg]o)|([Aa]ll )|(RT : )', "", b)
    return b

#Συνάρτηση σλυνδεσης στο tweeter
def Conector():
    # Προσπάθεια σύνδεσης στο API
    twitter_keys = {'consumer_key': 'GRiTt26hGO16RKRX18hPtZMq9',
                    'consumer_secret': '1n2FtYPZdcdVTnCT5wRghwTnpXtGmAdUfMuD4j8aLf0xNH216d',
                    'access_token_key': '1232017059128762368-3JPM79JJYmOB7edA8RMCOyknSXPVck',
                    'access_token_secret': 'zEXbCWChIab15NEY2zfhig6tepOs7EUiXI9feYyjapVAk'}
    print("Try to log in\n")
    # Setup access to API
    auth = OAuthHandler(twitter_keys['consumer_key'], twitter_keys['consumer_secret'])
    auth.set_access_token(twitter_keys['access_token_key'], twitter_keys['access_token_secret'])
    print("Log in achevied\n")
    return API(auth)

#Συνάτηση εξαγωγ΄ής στοιχείων
def GetUsersData(user_list):
    texter = {"user": [], "text": []}
    for users in user_list:
        print("****************************************************************")
        print(f"User id: {users.id}")
        print(f"Users followers count: {users.followers_count}")
        print(f"Περιγραφή χρήστη: {users.description}")
        print(f"Screen name χρήστη: {users.screen_name}")
        print(f"statuses_count: {users.statuses_count}")
        print(f"friends_count: {users.friends_count}")
        tweets = users.statuses_count
        account_created_date = users.created_at
        delta = datetime.utcnow() - account_created_date
        account_age_days = delta.days
        print(f"Ηλικία λογαρισμού [days]: {account_age_days}")
        if account_age_days > 0:
            print("Μ.Ο tweets ανά ημέρα: " + "%.2f" % (float(tweets) / float(account_age_days)))
        a = []
        # Συνδεωμαι στον καθε χρηστή μπαίνω στο timeline και παίρνω 50 tweets
        public_tweets = Cursor(api.user_timeline, id=users.id).items(NUM_OF_TWEETS)
        for tweet in public_tweets:
            a.append(tweet.text)
            # To αντικείμενο tweets έχει ολά τα παρακάτω κλειδία, για να τα δείς θέσε
            # NUM_OF_TWEETS=1
            # NUM_OF_USERS=1
            # και κάνε un-remark την παρακάτω γραμμή κώδικα
            # print(tweets._json.keys())
        text = ''
        for i in a:
            text = text + ' ' + i
        text = basicTextTrimming(text)
        texter["user"].append(users)
        texter["text"].append(text)
    return texter

#Συνάρτηση εύρεσης των περισσότερων λέξεων
def CmpText(dic):
    a = []
    for i in dic['text']:
        a.append(len(re.findall(r'\w+', i)))
    index = 0
    maxval = a[index]
    count = 0
    # print(a)
    for i in a:
        # print(i)
        if maxval < i:
            maxval = i
            index = count
        count = count + 1
    print(
        f"Ο χρήστης με το όνομα:'{dic['user'][index]._json['name']}' και screen name:'{dic['user'][index]._json['screen_name']}' μέσα σε πενήντα (50) tweets είχε τις περισσότερες λέξεις:{maxval}")
    # print(dic['user'][index]._json.keys())

#Κυριώς πρόγραμμα

try:
    api = Conector()
    try:
        users = [api.get_user(input("Παρακαλώ εισάγεται το id ένος tweeter user: ")) for i in
                 range(0, NUM_OF_USERS)]
        # Σημειώση @realDonaldTrump @normfinkelstein
        CmpText(GetUsersData(users))
    except:
        print("Σφάλμα κατά την εξαγωγή των tweets του χρήστη...")
except:
    print("Λάθος διαπευστήρια ή σφάλμα σύνδεσης...")
