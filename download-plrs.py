
import requests
from pprint import pprint
import string
import time
import os, sys
import wget
import urllib



course_name = input("Course name --> ")
cookie = input("Cookie --> ")
resolution = input('Resolution -->')

headers = {
    'origin': 'https://app.pluralsight.com',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,hi;q=0.8,mr;q=0.7',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'content-type': 'application/json;charset=UTF-8',
    'accept': '*/*',
    'authority': 'app.pluralsight.com',
    'cookie': cookie,
}

data = '{"query":"\\n        query BootstrapPlayer {\\n          rpc {\\n            bootstrapPlayer {\\n              profile {\\n                firstName\\n                lastName\\n                email\\n                username\\n                userHandle\\n                authed\\n                isAuthed\\n                plan\\n              }\\n              course(courseId: \\"'+course_name+'\\") {\\n                name\\n                title\\n                courseHasCaptions\\n                translationLanguages {\\n                  code\\n                  name\\n                }\\n                supportsWideScreenVideoFormats\\n                timestamp\\n                modules {\\n                  name\\n                  title\\n                  duration\\n                  formattedDuration\\n                  author\\n                  authorized\\n                  clips {\\n                    authorized\\n                    clipId\\n                    duration\\n                    formattedDuration\\n                    id\\n                    index\\n                    moduleIndex\\n                    moduleTitle\\n                    name\\n                    title\\n                    watched\\n                  }\\n                }\\n              }\\n            }\\n          }\\n        }\\n      ","variables":{}}'


response = requests.post('https://app.pluralsight.com/player/api/graphql', headers=headers, data=data)

json_data =  response.json()

module_list = json_data["data"]["rpc"]["bootstrapPlayer"]["course"]["modules"]





headers = {
    'origin': 'https://app.pluralsight.com',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,hi;q=0.8,mr;q=0.7',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'content-type': 'application/json;charset=UTF-8',
    'accept': '*/*',
    'authority': 'app.pluralsight.com',
    'cookie': cookie,
}

raw_data = '{"query":"\\n query viewClip {\\n viewClip(input: {\\n author: \\"{{author}}\\", \\n clipIndex: {{clipIndex}}, \\n courseName: \\"{{courseName}}\\", \\n includeCaptions: false, \\n locale: \\"en\\", \\n mediaType: \\"webm\\", \\n moduleName: \\"{{moduleName}}\\", \\n quality: \\"'+resolution+'\\"\\n }) {\\n urls {\\n url\\n cdn  \\n rank\\n source\\n },\\n status \\n }\\n }\\n ","variables":{}}'
final_download_list = []

for index, module in enumerate(module_list):
    updated_stgring = raw_data.replace("{{author}}", module["author"])
    updated_stgring = updated_stgring.replace("{{courseName}}", course_name)
    updated_stgring = updated_stgring.replace("{{moduleName}}", module["name"])
    
    module_name = str(index+1)+"-"+module["title"]
    pprint("Fetching data for module --> "+module_name)
    pprint("###########################################################################################")
    download_video_module = {
        'module_name': module_name,
        'clip_list':[]
    }   
    for index, clip in enumerate(module["clips"]):
        pprint("Fetching data for clip --> "+clip['title'])
        final_updated_stgring = updated_stgring.replace("{{clipIndex}}", str(index))
        response2 = requests.post('https://app.pluralsight.com/player/api/graphql', headers=headers, data=final_updated_stgring)
        data = response2.json()
        
        download_video_clip = {
            'clip_name': clip['title'],
            'url': data["data"]["viewClip"]["urls"][0]["url"]
        }
        download_video_module['clip_list'].append(download_video_clip) 
        time.sleep(1)
    pprint("###########################################################################################")
    
    final_download_list.append(download_video_module)
    if index == 1:
        break
    time.sleep(1)
   


os.makedirs(course_name)
for index, module in enumerate(final_download_list):
    path = course_name+'/'+module['module_name']
    os.makedirs(path)
    print("----------------------------------------------------------------------------------------------")
    print("Downloading "+str(index+1)+"/"+str(len(final_download_list)+1)+" module")
    print("----------------------------------------------------------------------------------------------")
    for index, clip in enumerate(module["clip_list"]):
        print("Downloading "+str(index+1)+"/"+str(len(module["clip_list"])+1)+" clip")
        wget.download(clip['url'],path+'/'+str(index+1)+'-'+clip['clip_name'].replace("/","-")+'.webm')
        print("\n")


