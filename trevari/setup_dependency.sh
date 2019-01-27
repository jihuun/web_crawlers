
# python2.7 & modules
sudo apt-get install python2.7
sudo ln -s python2.7 /usr/bin/python
sudo apt-get install python-pip python-dev python-setuptools
pip install requests BeautifulSoup4 selenium

# Install Chrome.
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list #안되면 수동으로
sudo apt-get -y update
sudo apt-get -y install google-chrome-stable

# Install chrome driver
sudo apt-get install -y unzip openjdk-8-jre-headless xvfb libxi6 libgconf-2-4
wget https://chromedriver.storage.googleapis.com/2.45/chromedriver_linux64.zip
