import praw
import urllib.request
import re
import json
import os

def get_urls():
  saved = r.user.get_saved(limit=None)
  urls = {}

  for link in saved:
    if isinstance(link, praw.objects.Submission) and not link.is_self:
      #print(link.title.encode('utf-8'))
      urls[link.url] = link.subreddit.display_name
  
  return urls
    
def fix_urls(urls):
  fixed_urls = {}
  add = ''
  
  for url in urls:
    #print(url)
    if 'imgur.com' in url and '/a/' not in url:
      if '.jpg' not in url and '.png' not in url and '.gif' not in url and '/a/' not in url:
        add = url + '.jpg'
      elif '.gifv' in url:
        add = url.replace('gifv', 'mp4')
      else:
        add = url.split('?')[0]
    elif 'gfycat.com' in url:
      if '.gif' not in url and '.webm' not in url and '.mp4' not in url:
        name = url.split('/')[-1]
        try:
          response = urllib.request.urlopen('https://gfycat.com/cajax/get/' + name).read().decode('utf-8')
          data = json.loads(response)
          add = data['gfyItem']['webmUrl']
        except Exception:
          print('  Could not add ' + name + '. It probably was deleted.')
          pass
      else:
        add = url
    elif re.match('.*\.(jpg|png|gif|webm)', url):
      add = url
    else:
      add = 'null'
    
    if add != 'null':
      fixed_urls[add] = urls[url]
      #print(add)
  
  return fixed_urls
  
def download_urls(urls, dir):
  if not os.path.exists(dir):
    os.makedirs(dir)
  #if not os.path.exists(dir + subdirs):
  #  os.makedirs(dir + subdirs)
    
  for url in urls:
    file_name = url.split('/')[-1]
    print('Downloading: ' + url)
    path = dir
    try: 
      urllib.request.urlretrieve(url, path + file_name)
    except Exception:
      print('  Could not download ' + url)
      pass
    
#main
username = input("Username: ")
password = input("Password: ")

r = praw.Reddit('testing API stuff')
r.login(username, password, disable_warning=True)
print('Logging in...')

saved = get_urls()
print('Getting image links...')

fixed = fix_urls(saved)
#print('\n')
dir = input("Image directory name: ")
dir = dir + '/'
download_urls(fixed, dir)
print('Done!')