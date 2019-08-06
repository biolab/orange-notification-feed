#!/bin/sh

setup_git() {
  git config --global user.email "travis@travis-ci.org"
  git config --global user.name "Travis CI"
}

commit_website_files() {
  git fetch origin generated-feed:generated-feed
  git checkout generated-feed
  rm feed.yaml
  mv tmpfeed.yaml feed.yaml
  git add feed.yaml
  git commit --message "Travis build: $TRAVIS_BUILD_NUMBER"
}

upload_files() {
  git remote add irgolic https://${GH_TOKEN}@github.com/irgolic/orange-notification-feed.git > /dev/null 2>&1
  git push -f --set-upstream irgolic generated-feed 
}

setup_git
commit_website_files
upload_files
