#!/bin/sh


cmdname="$(basename "$0")"
bin_path="$(cd "$(dirname "$0")" && pwd)"
repo_path="${bin_path}/.."


usage() {
    cat << USAGE >&2
Usage:
    $cmdname [-h|--help] [ansible-pull options]
    -h     Show this help message
    Wrapper for ansible-pull
    Install dependencies and run ansible-pull with defaults
USAGE
    exit 1
}

die(){
    printf '%s\n' "$1" >&2
    exit 1
}


ARGS=$@

while :; do
    case $1 in
        -h|-\?|--help)
            usage
            exit
            ;;
        # handle checkout dir option
        -d|--directory)
            test "$2" || die "ERROR: $1 requires a non-empty option argument."
            checkout_dir=$2
            shift
            ;;
        -d*)
            # Delete "-d" and assign the remainder
            checkout_dir=${1#*-d}
            ;;

        --directory=?*)
            # Delete everything up to "=" and assign the remainder
            checkout_dir=${1#*=}
            ;;

        # handle repo URL option
        -U|--url)
            test "$2" || die "ERROR: $1 requires a non-empty option argument."
            repo_url=$2
            shift
            ;;
        -U*)
            repo_url=${1#*-U}
            ;;
        --url=?*)
            repo_url=${1#*=} 
            ;;
        "")
            # no more options
            break
            ;;
    esac
    shift
done

default_checkout_dir=/tmp/ansible
checkout_dir="${checkout_dir:-$default_checkout_dir}"

PATH="${PATH}:${HOME}/.local/bin"



if [ ! -d "$checkout_dir" ]; then
    git clone "$repo_url" "$checkout_dir"
fi

# assume directory to checkout repository to contains requirements.yaml or requirements.yml
ansible-galaxy install --role-file="$checkout_dir"/requirements.yaml
ansible-pull $ARGS
