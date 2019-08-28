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
        -d|--directory)       # Takes an option argument; ensure it has been specified.
            test "$2" || die 'ERROR: "--directory" requires a non-empty option argument.'
            checkout_dir=$2
            shift
            ;;
        --directory=?*)
            checkout_dir=${1#*=} # Delete everything up to "=" and assign the remainder.
            ;;

        # handle repo URL option
        # Takes an option argument; ensure it has been specified.
        -U|--url)       
            test "$2" || die 'ERROR: "--url" requires a non-empty option argument.'
            repo_url=$2
            shift
            ;;
        --url=?*)
            # Delete everything up to "=" and assign the remainder.
            repo_url=${1#*=} 
            ;;


        # Default case: No more options, so break out of the loop.
        *)
            break
    esac
    shift
done

PATH="${PATH}:${HOME}/.local/bin"



if [ ! -d "$checkout_dir" ]; then
    git clone "$repo_url" "$checkout_dir"
fi

# assume directory to checkout repository to contains requirements.yaml or requirements.yml
ansible-galaxy install --role-file="$checkout_dir"/requirements.yaml
ansible-pull $ARGS
