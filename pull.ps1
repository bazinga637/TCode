# THIS SCRIPT WILL DELETE EVERYTHING AFTER CLONING
# navigate to folder to clone to and run git clone, any further updates will use git pull

git clone https://github.com/bazinga637/TCode.git ../TCodetemp/TCode # clone to temp folder

git pull origin main

Move-Item -Path "C:\home\mjkstra\Documents\TCodetemp\TCode" -Destination "C:\home\mjkstra\Documents" -Force # replace from temp folder to actual folder
