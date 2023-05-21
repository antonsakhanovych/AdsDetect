#/usr/bin/env bash

cd api
npm install

cd ../model
pip3 install -r requirements.txt
pip3 install scikit-learn
pip3 install Levenshtein