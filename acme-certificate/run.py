#!/usr/bin/python
import json, os, shutil, signal, subprocess, time
from pprint import pprint
from glob import glob

json_data = None
config_dir = None
user_email = None

def ProcessTopLevel(domain):
    main_domain = domain["domain"]
    envs = domain["environment"]
    environment = os.environ
    environment["LE_WORKING_DIR"] = config_dir
    environment["DEPLOY_LOCALCOPY_RELOADCMD"] = "/notify.sh"
    environment["DEPLOY_TARGET"] = main_domain
    issue_opts = domain["issue_options"]
    ## --debug 2
    issue_options = [config_dir + "/acme.sh", "--issue", "-d", main_domain, "--log"]
    deploy_opts = domain["deploy_options"]
    deploy_options = [config_dir + "/acme.sh", "--deploy", "-d", main_domain, "--log"]

    print ("Process: " + main_domain)
    stamp = time.time()

    for env in envs: 
        opt = env.split("=", 1)
        environment[opt[0]] = opt[1]
    print(environment)

    for opt in issue_opts:
        strs = opt.split()
        issue_options.extend(strs)
    print(issue_options, flush=True)

    p = subprocess.Popen(issue_options, cwd= config_dir, env= environment)
    p.wait()
    print("Cheching for:" + main_domain + "*" + " in " + config_dir, flush=True)
    for dir in glob(main_domain + "*", root_dir=config_dir):
        cert_dir = config_dir + "/" + dir
        if os.path.getmtime(cert_dir) > stamp:
            fullchain = cert_dir + "/" + "fullchain.cer"
            print("Checking for new cert in:" + cert_dir)
            if os.path.exists(fullchain):
                print("File exists:" + fullchain)
                if os.path.getmtime(fullchain) > stamp:
                    for opt in deploy_opts:
                        strs = opt.split()
                        deploy_options.extend(strs)
                    print(deploy_options, flush=True)
                    p = subprocess.Popen(deploy_options, cwd= config_dir, env= environment)
                    p.wait()

print("Starting acme.sh Certificates addon!", flush=True)

if os.path.exists('/data/options.json'):
    with open('/data/options.json', 'r') as json_file:
        json_data = json.load(json_file)
        json_file.close()
        pprint(json_data)
        print("", flush=True)

if json_data:
    config_dir = "/config/" + json_data["config_sub_dicrectory"]
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

    user_email = json_data["email"]
    if user_email:
        p = subprocess.Popen(["./acme.sh", "--install", "--no-cron", "--home", config_dir, "-m", user_email], cwd="/acme.sh")
        p.wait()

        local_deploy = config_dir + "/deploy/localcopy.sh"
        if not os.path.exists(local_deploy):
            shutil.copy2("/localcopy.sh", local_deploy)

        domains = json_data["domains"]
        for domain in domains:
            ProcessTopLevel(domain)

        while True:
            time.sleep(3600 * 48)
            print("Cron Processing", flush=True)
            p = subprocess.Popen(["./acme.sh", "--cron", "--home", config_dir], cwd= config_dir)
            p.wait()

signal.pause()