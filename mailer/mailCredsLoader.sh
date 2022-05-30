#! /bin/bash

if [[ $# -lt 2 ]]
then
  echo "Usage: $0 <SMTP Configfile> <Script> <Function Type> <Other Options>"
  exit 1
fi

SMTP_FILE=$1
shift
SCRIPT=$1
shift
FUNCTION_TYPE=$1
shift

eval "$(sed 's/\r$//' "${SMTP_FILE}")"

commandOptions=$(python "${SCRIPT}" "${FUNCTION_TYPE}" --help | grep -A100 options | grep "imap\|smtp" | awk '{print $1}')
commandOptions=( $commandOptions )
command=("python" "${SCRIPT}" "${FUNCTION_TYPE}")
for option in "${commandOptions[@]}"
do
    optionEnv=${option:2}
    optionEnv=$(echo $optionEnv | sed -r 's/([a-z0-9])([A-Z])/\1_\L\2/g' | tr '[a-z]' '[A-Z]')
    command+=("${option}" "${!optionEnv}")
done

"${command[@]}" "$@"