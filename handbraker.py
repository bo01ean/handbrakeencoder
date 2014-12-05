#!/usr/bin/python
#  handbrakeencoder
#  Recursively encode video files with HandbrakeCLI
#  chmod +x
#  Created by boolean ( bo01ean ) github.com/bo0lean on raptor on 6/9/14.
#

import os, re
from subprocess import *


## REGEX pattern we use to look for video files
videoPattern = re.compile(r"\.(mov|mpeg|mpg|mkv|avi)$", re.I)
## Path to HandbrakeCLI binary
handbrakeBinary = "/Applications/HandBrakeCLI"
## HandbrakeCLI profile we want to use ( HandbrakeCLI --preset-list ):
preset = "High Profile"
## Where do we start from?
topDirectory = "~/Dropbox/Photos/"
## Set this if you want to nuke files after successfully encoding
nukeOriginalFiles  = True

"""
    In case we can't find handbrake goto download page
    """
def gotoDownload():
    print "HandBrakeCLI '{0}' not found. Please download from: http://handbrake.fr/downloads2.php".format(handbrakeBinary)
    call("open 'http://handbrake.fr/downloads2.php'", shell=True)
"""
    Encode the files with preset
    """
def encode(src):
    dest = re.sub(videoPattern, ".m4v", src)
    print "Encode: ", src, '->',  dest
    call(["/bin/rm", "-f", dest]);
    cmd = "{0} --preset='{1}' -i '{2}' -o '{3}'".format(handbrakeBinary, preset, src, dest)
    print cmd
    if check_call(cmd, shell=True) == 0:
        if (nukeOriginalFiles):
            print "Deleting '{0}'".format(src)
            call("/bin/rm -f '{0}'".format(src), shell=True)
"""
    Recurse FileSystem looking for files that match REGEX videoPattern
    """
def walkit(top="~/Dropbox/Photos/"):
    print "recursing into: '{0}'".format(top)
    for dirpath, dnames, fnames in os.walk(top):
        for f in fnames:
            path = os.path.join(dirpath, f)
            if videoPattern.findall(path):
                print path, "match!"
                encode(path)

"""
    Check input, and walk through files
    """
def main():
    global nukeOriginalFiles
    if nukeOriginalFiles == True:
        nukeOriginalFiles = raw_input("Are you sure you want to nuke the original files? Press 1 for yes, or 0 for no: ")
        nukeOriginalFiles = True if nukeOriginalFiles == "1" else False
        
        print "Nuking Fles: ", nukeOriginalFiles
    if not os.path.isfile(handbrakeBinary) and not os.access(handbrakeBinary, os.X_OK):
        gotoDownload()
    else:
        walkit(topDirectory)


if __name__ == "__main__":
    main()
