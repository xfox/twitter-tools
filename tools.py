from xml.etree import ElementTree
import urllib
import re

load_friends = 'http://%s:%s@api.twitter.com/1/friends/ids.xml'
load_followers = 'http://%s:%s@api.twitter.com/1/followers/ids.xml' 
destroy_friendship = "http://%s:%s@api.twitter.com/1/friendships/destroy.xml?id=%s"
create_friendship = 'http://%s:%s@api.twitter.com/1/friendships/create.xml?screen_name=%s'
create_friendship_id = 'http://%s:%s@api.twitter.com/1/friendships/create.xml?id=%s'

class TwitterTool(object):

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def loadfriends(self):
        fp = urllib.urlopen(load_friends % (self.login, self.password))
        friends = ElementTree.XML(fp.read())

        fp = urllib.urlopen(load_followers % (self.login, self.password))
        followers = ElementTree.XML(fp.read())

        self.friends = set([ id.text for id in friends.findall('id')])
        self.followers = set([ id.text for id in followers.findall('id')])

        print "Total friends: %s\nTotal followers: %s\n" % (len(friends), len(followers))
        print "Non mutal: %s\n" % len(self.friends - self.followers)

    def print_result(self, fp):
        print ElementTree.XML(fp.read()).find('screen_name').text + ' '

    def follow_back(self):
        print "Need to follow back: %s" % len(self.followers - self.friends) 
        for id in self.followers - self.friends: 
            fp = urllib.urlopen(create_friendship_id % (self.login, self.password, id), data='a=1')
            self.print_result(fp)

    def remove_nonfollowers(self, count):
        index = 0
        for id in self.friends - self.followers:
            fp = urllib.urlopen(destroy_friendship % (self.login, self.password, id), data='a=1')
            self.print_result(fp)
            index +=1
            if index >= count:
                break

    def find_followers(self, page):
        raw_html = urllib.urlopen('http://www.rutwitter.com/r/?page=%s' % page).read()
        for nick in re.findall("href=http://twitter.com/([a-z0-9\_\-]+)", raw_html):
            fp = urllib.urlopen(create_friendship % (self.login, self.password, nick), data='a=1')
            self.print_result(fp)


if __name__ == '__main__':
    login = raw_input('login: ')
    password = raw_input('password: ')

    tool = TwitterTool(login, password)
    tool.loadfriends()

    tool.follow_back()

    count = int(raw_input('how many to delete: '))

    tool.remove_nonfollowers(count)

    page = raw_input('page to follow: ')

    tool.find_followers(page)