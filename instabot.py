import requests, urllib
from textblob import TextBlob       # For Sentiment Analysis the library TextBlob is used
from textblob.sentiments import NaiveBayesAnalyzer

APP_ACCESS_TOKEN = '5708214805.2424d36.39486f8497c642028688f266eb69750d'    #APP_ACCESS_TOKEN is a global variable
#Token owner: pl_instabot
#Sandbox Users : shoetho, love_with_destinations

BASE_URL = 'https://api.instagram.com/v1/'      #BASE_URL is a global variable


def self_info():        #Function declaration to get your own info
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'Followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'Following: %s' % (user_info['data']['counts']['follows'])
            print 'Posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 received!'


def get_user_id(insta_username):         #Function declaration to get the ID of a user by username
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit()


def get_user_info(insta_username):          #Function declaration to get the info of a user by username
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'Followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'Following: %s' % (user_info['data']['counts']['follows'])
            print 'Posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'


def get_own_post():         #Function declaration to get your recent post
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'


def get_user_post(insta_username):          #Function declaration to get the recent post of a user by username
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'


def get_post_id(insta_username):        #Function declaration to get the ID of the recent post of a user by username
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()


def get_like_list(insta_username):      #Function declaration to get the list of users who liked the post.
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    likes_info = requests.get(request_url).json()

    if likes_info['meta']['code'] == 200:
        if len(likes_info['data']):
            for x in range(0, len(likes_info['data'])):
                print likes_info['data'][x]['username']
        else:
            print 'No user has liked the post yet!'
    else:
        print 'Status code other than 200 received!'


def like_a_post(insta_username):        #Function declaration to like the recent post of a user
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": APP_ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'
    else:
        print 'Your like was unsuccessful. Try again!'


def get_comment_list(insta_username):       #Function declaration to get the list of users who commented on the post.
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            for x in range(0, len(comment_info['data'])):
                print 'Comment: %s || User: %s' % (comment_info['data'][x]['text'],
                                                   comment_info['data'][x]['from']['username'])
        else:
            print 'There are no comments on this post!'
    else:
        print 'Status code other than 200 received!'


def post_a_comment(insta_username):     #Function declaration to make a comment on the recent post of the user
    media_id = get_post_id(insta_username)
    comment_text = raw_input("Your comment: ")
    payload = {"access_token": APP_ACCESS_TOKEN, "text" : comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)

    make_comment = requests.post(request_url, payload).json()

    if make_comment['meta']['code'] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"


def delete_negative_comment(insta_username): #Function declaration to make delete negative comments from the recent post
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            #Naive implementation to delete the negative comments
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s')\
                                 % (media_id, comment_id, APP_ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'
                else:
                    print 'Positive comment : %s\n' % (comment_text)
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'


def get_media_of_your_choice(insta_username):       #Function to fetch users any post
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'user does not exist'
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    user_media = requests.get(request_url).json()
    if user_media['meta']['code'] == 200:
        if len(user_media['data']):

            post_number = raw_input("enter no of post which you want : ")
            post_number = int(post_number)

            x = post_number - 1
            image_name = user_media['data'][x]['id'] + '.jpeg'
            image_url = user_media['data'][x]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print'User media does not exist'
    else:
        print 'Status code error!'


def target_comments(insta_username):            #Takes argument as insta username
    user_id = get_user_id(insta_username)       #URL of tags has been used
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    caption_info = requests.get(request_url).json()

    if caption_info['meta']['code'] == 200:

        if len(caption_info['data']):

            for y in range(0, len(caption_info['data'])):

                caption_text = str(caption_info['data'][y]['caption'])
                caption = caption_text.split(' ')
                if '#shoe' in caption:
                    print 'Read Caption: %s' % (caption)
                    media_id = get_post_id(insta_username)
                    comment_text = 'Nice shoes! Visit our page for some kickass shoes.'
                    payload = {'access_token': APP_ACCESS_TOKEN, "text": comment_text}
                    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
                    print 'POST request url : %s' % (request_url)

                    make_comment = requests.post(request_url, payload).json()

                    if make_comment['meta']['code'] == 200:

                        print 'Successfully Posted Targeted Comment!'
                    else:
                        print 'Unable to add comment. Try again!'
                else:
                    print 'No caption on the post!'

        else:

            print 'Status code other than 200 received!'
    exit()


def start_bot():
    while True:
        print '\n'
        print 'Welcome to instaBot!'
        print 'Menu options:'
        print "a.Get your own details\n"
        print "b.Get details of a user by username\n"
        print "c.Get your own recent post\n"
        print "d.Get the recent post of a user by username\n"
        print "e.Get a list of people who have liked the recent post of a user\n"
        print "f.Like the recent post of a user\n"
        print "g.Get a list of comments on the recent post of a user\n"
        print "h.Make a comment on the recent post of a user\n"
        print "i.Delete negative comments from the recent post of a user\n"
        print "j.Get any post of a user\n"
        print "k.Marketing\n"
        print "l.Exit"


        choice = raw_input("Enter you choice: ")
        if choice == "a":
            self_info()
        elif choice == "b":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_info(insta_username)
        elif choice == "c":
            get_own_post()
        elif choice == "d":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_post(insta_username)
        elif choice=="e":
           insta_username = raw_input("Enter the username of the user: ")
           get_like_list(insta_username)
        elif choice=="f":
           insta_username = raw_input("Enter the username of the user: ")
           like_a_post(insta_username)
        elif choice=="g":
           insta_username = raw_input("Enter the username of the user: ")
           get_comment_list(insta_username)
        elif choice=="h":
           insta_username = raw_input("Enter the username of the user: ")
           post_a_comment(insta_username)
        elif choice=="i":
           insta_username = raw_input("Enter the username of the user: ")
           delete_negative_comment(insta_username)
        elif choice == 'j':
            insta_username = raw_input("enter username of the user : ")
            get_media_of_your_choice(insta_username)
        elif choice == 'k':
            insta_username = raw_input("Enter the username: ")
            target_comments(insta_username)
        elif choice == 'l':
            exit()
        else:
            print "Wrong choice!"

start_bot()