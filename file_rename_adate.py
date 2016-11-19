# Script to append modification date to files
import os
import time


cdir = '~/'
ftype = '.pdf'
files = [f for f in os.listdir(cdir) if f[-4:] == ftype]

DRYRUN = True
print "Dryrun = %s" % DRYRUN

for filename in files:
    extension = os.path.splitext(filename)[1]
    ffilename = os.path.join(cdir, filename)
    mtime = os.path.getmtime(ffilename)
    smtime = time.strftime("%Y-%m-%d", time.localtime(mtime))
    newname = "New Name %s%s" % (smtime, extension)
    if os.path.exists(newname):
        print "Cannot rename %s to %s, already exists" % (filename, newname)
        continue
    if DRYRUN:
        print "Would rename %s to %s" % (filename, newname)
    else:
        print "Renaming %s to %s" % (filename, newname)
        os.rename(ffilename, os.path.join(cdir, newname))
