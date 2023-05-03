# ansible-bootstrap
Personal Infrastructure managed via ansible

# Setup
## Enable Ansible Management
To manage a new host, add its hostname to any relevant groups in `hosts.ini`

### Enable Persistent Management
To enable persistent management (via ansible-pull), add the new host to the `ansible_pull_managed` group

# Running
First, run any steps in [Setup](#Setup) as necessary

## Pull
To run ansible in pull-mode, invoke ansible-pull on the desired host:

    ansible-pull --url https://github.com/ivan-c/ansible-bootstrap

## Push
To connect and run ansible on a remote host, invoke ansible as follows:

    ansible-playbook --limit $HOST local.yml
