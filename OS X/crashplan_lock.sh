# Commands to resolve issues caused by CrashPlan.app being locked
# see https://discussions.apple.com/thread/5750388?start=15&tstart=0

# Unlock all local expired backup copies of CrashPlan
sudo find /.MobileBackups.trash -flags +schg -exec chflags noschg {} \;

# Unlock all backup copies of CrashPlan;
# need to run from Time Machine machine directory
# (e.g. /Volumes/MyExternalHD/Backups.backupdb/MyMac/)
find . -maxdepth 1 -type d -exec \
    sudo /System/Library/Extensions/TMSafetyNet.kext/Contents/Helpers/bypass \
    chflags noschg "{}"/Macintosh\ HD/Applications/CrashPlan.app \;

# Unlock CrashPlan application
sudo chflags noschg /Applications/CrashPlan.app
# Or exclude CrashPlan from backups
sudo tmutil addexclusion /Applications/CrashPlan.app
