rm -rf outgoing/
currentBranch=$(git branch --show-current)
echo "Current Branch: $currentBranch"
commitCount=$(git rev-list --count $currentBranch ^origin/$currentBranch)
echo "Branch is behing origin by $commitCount commits"
git format-patch -o outgoing/ -$commitCount
