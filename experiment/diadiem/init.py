import os

os.system("rm -rf etc")
os.system("rm -rf logdir")
os.system("rm -rf *.html")
os.system("rm -rf wav")
os.system("sphinxtrain -t diadiem setup")