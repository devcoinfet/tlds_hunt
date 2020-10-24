import requests
import os
import sys
import threading
import subprocess

main_url = "https://raw.githubusercontent.com/umpirsky/tld-list/master/data/en/tld.json"

total_domains = []
def get_tlds(url,domain):
    domains_generated = []
    r = requests.get(url,timeout=10,verify=False)
    if r:
       print(type(r.json()))
       for key in r.json():
           if len(key) > 2:
              pass
           else:
               '''
               domain + .co.tld
               domain + .com.tld
               domain + tld
               example.it would be domain + tld
               example.com.it would be domain + .com.tld

               example.co.it would be domain + .co.tld
               so smart move here is to pass the org in like this
               python3 tldnew.py sony or starbucks etc it will generate domains per mutations below
               '''
               tmp_domain = domain +"." + key
               tmp_domain2 = domain +".co." + key 
               tmp_domain3 = domain +".com." + key 
               domains_generated.append(tmp_domain)
               domains_generated.append(tmp_domain2)
               domains_generated.append(tmp_domain3)
    return domains_generated


def get_subfinder_data(target_domain):
    cmd = "assetfinder -subs-only " + target_domain.strip()
    print(cmd)
    sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ""
    while True:
        out = sp.stdout.read(1).decode('utf-8')
        if out == '' and sp.poll() != None:
           break
        if out != '':
           output += out
           sys.stdout.write(out)
           sys.stdout.flush()

    if output:
       return output
       
       
                



def main():
    domains_generated = get_tlds(main_url,sys.argv[1])
    if domains_generated:
       print(domains_generated)
   
       for domains in domains_generated:
           try:
              output = get_subfinder_data(domains)
              if output:
                 domains_located = output.split()
                 total_domains.extend(domains_located)
           except Exception as ex:
             print(ex)
             pass
    fileout = open("infodomains.txt","a") 
    print("Found {} Total Domains".format(str(len(total_domains))))
    print("*" *50)
    for domain in total_domains:
        fileout.write(str(domain)+"\n")
    fileout.close()


main()
