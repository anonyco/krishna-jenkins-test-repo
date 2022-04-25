currentBranch=$(git branch --show-current)

echo $currentBranch

commitCount=$(git rev-list --count $currentBranch ^origin/$currentBranch)

echo $commitCount
