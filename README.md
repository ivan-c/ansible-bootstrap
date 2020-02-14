ansible-bootstrap
=================
Infrastructure managed via ansible pull-mode

Enable Ansible Management
-------------------------
To manage a host via ansible-pull follow the below steps

Download and run [this script](https://gist.github.com/ivan-c/35768f1ee268ce0a581f412bffa8a3dc) to install the latest version of ansible and its dependencies

    wget \
        --output-document /tmp/bootstrap-ansible.sh \
    https://gist.githubusercontent.com/ivan-c/35768f1ee268ce0a581f412bffa8a3dc/raw/bootstrap-ansible.sh
    chmod +x /tmp/bootstrap-ansible.sh

    /tmp/bootstrap-ansible.sh

Download and run [this wrapper for ansible-pull](https://github.com/ivan-c/ansible-role-ansible-pull/blob/master/files/ansible_pull_wrapper.sh), substituting `$REPO_URL` with the desired playbook URL

    wget \
        --output-document /usr/bin/ansible_pull_wrapper.sh \
    https://raw.githubusercontent.com/ivan-c/ansible-role-ansible-pull/master/files/ansible_pull_wrapper.sh
    chmod +x /usr/bin/ansible_pull_wrapper.sh

    ansible_pull_wrapper.sh --tags boot --url $REPO_URL
