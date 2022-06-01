rm -rf outgoing/
currentBranch=$(git branch --show-current)
echo "Current Branch: $currentBranch"
commitCount=$(git rev-list --count $currentBranch ^origin/$currentBranch)
echo "Branch is behing origin by $commitCount commits"
echo "Pushing $commitCount commits to Build server"
git format-patch -o outgoing/ -$commitCount

python mailer/mailer.py patchFormatter --path outgoing/ --branch $currentBranch
git send-email --to="krishna@git.rightend.com" outgoing/*