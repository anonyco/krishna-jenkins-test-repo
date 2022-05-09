BRANCH=$(git branch --show-current)
git stash
git pull
git reset --hard origin/$BRANCH
git stash apply
