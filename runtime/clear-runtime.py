#!/usr/bin/python3

# HomeCloud
# > Helpers > Runtime Cleanup
#
# Generates the files you can place for the provisioned instance
# Author: Narcis.IO <n@narcis.io>

import datetime
import sys
import os

if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")
    
if os.path.basename(os.getcwd()) != "runtime":
    exit("Please cd into ./runtime first")

class YWLRemove:
    cnt_dir = 0
    cnt_files = 0

    def y_log(self, msg):
        print("%s: %s" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg))

    def y_rm(self, folder):
        import os, shutil

        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if the_file.find(".git_empty") == -1 and the_file.find("git.empty") == -1 and (os.path.isfile(file_path) or os.path.islink(file_path)):
                    self.y_log("    [F] Removing file %s" % file_path)
                    os.unlink(file_path)
                    self.cnt_files += 1
                elif os.path.isdir(file_path): 
                    self.y_log("    [D] Removing directory %s" % file_path)
                    shutil.rmtree(file_path)
                    self.cnt_dir += 1
            except Exception:
                raise

    def process(self):
        if input("Remove MySQL directory (y/n)? ") == "y":
            self.y_log("Removing ./mysql")
            self.y_rm("./mysql")


        self.y_log("[DONE] Removed %d files and %d directories" % (self.cnt_files, self.cnt_dir))

YWLRemove().process()
