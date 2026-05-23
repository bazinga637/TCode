# THIS SCRIPT WILL DELETE EVERYTHING AFTER CLONING
# navigate to folder to clone to and run git clone, any further updates will use git pull

git clone https://github.com/bazinga637/TCode.git ../temp/TCode # clone to temp folder

git pull origin main

Move-Item -Path "\home\mjkstra\Documents\temp\TCode" -Destination "\home\mjkstra\Documents" -Force # replace from temp folder to actual folder
