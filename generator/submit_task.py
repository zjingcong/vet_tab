#!/usr/bin/env python

import os
import paramiko
import threading
import time

RENDER = '/home/jingcoz/workspace/vetTab_robustness/ssh_test/test.py'
SCENE_PATH = '/DPA/jedi/zjingcong/vet_tab/scenes/test_ssh_scene'
LOG_PATH = '/DPA/jedi/zjingcong/vet_tab/scenes/test_ssh_scene'
HOST = '{name}.cs.clemson.edu'

host_dict = {'ada': range(1, 18),
             'joey': range(2, 21),
             'koala': range(1, 23),
             'titan': range(1, 6)}

###########################

# get hosts list
host_list = []
for key, value in host_dict.iteritems():
    host_list += list(map(lambda x: HOST.format(name=key + str(x)), value))
print "Get hosts info."

# get scene files list
getscenecmd = 'ssh -t jingcoz@koala1.cs.clemson.edu ls {}'.format(SCENE_PATH)
result = os.popen(getscenecmd).read().split('\n')
num = len(result) - 1
scene_list = result[:num]
scene_list = [filename for filename in result[:num] if filename.split('.')[-1]=='pbrt']
print "Get scene files info."

###########################

user = 'jingcoz'
pw = 'zjc_APTX4869'
command = "nohup {renderer} {scene} | tee {log}"

lock = threading.Lock()
host_thread = dict()


def workon(host, scene_file, log_file):
    # set ssh client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=user, password=pw)
    stdin, stdout, stderr = client.exec_command(command.format(renderer=RENDER, scene=scene_file, log=log_file))
    stdin.close()
    # acquiring lock
    with lock:
        print '\n'.join(stdout.readlines())
        client.close()
        print "Render task {} complete on host {} complete.".format(scene_file, host)


def start_thread(hostname):
    # all the scene files complete
    if not scene_list:
        return (True, threading.Thread())

    # still have unrendered scene file
    scene = scene_list.pop()
    scene_file = os.path.join(SCENE_PATH, scene)
    log_file = os.path.join(LOG_PATH, '{}.log'.format(scene_file))

    t = threading.Thread(target=workon, args=(hostname, scene_file, log_file))
    t.start()
    print "Thread host: ", hostname
    print "\tRender scene file: {}".format(scene_file)
    print "\tRender log file: {}".format(log_file)
    return (False, t)


def main():
    print "Submit render tasks..."
    print "=" * 100
    hosts = host_list
    for hostname in hosts:
        is_complete, t = start_thread(hostname)
        host_thread[hostname] = t

    # keep submitting render tasks to hosts
    isComplete = is_complete
    while not isComplete:
        time.sleep(2)
        for hostname, t in host_thread.iteritems():
            if not isComplete:
                # host is idle
                if t.isAlive() is False:
                    is_complete, t = start_thread(hostname)
                    isComplete = is_complete

    # wait until all the render tasks finished
    clientOn = True
    while clientOn:
        if threading.activeCount() <= 1:
            clientOn = False

    print "=" * 100
    print "Complete all the render tasks."

# run
main()
