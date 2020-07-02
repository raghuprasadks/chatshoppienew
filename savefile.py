import subprocess

with open("test2.json","w+") as output:
    subprocess.call(["python",r"C:\Users\Anup\OneDrive\AMQ_Master2\ebaytest.py"],stdout=output)


print ("sucess")