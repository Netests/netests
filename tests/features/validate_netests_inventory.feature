Feature: Test Python class netests/tools/verify/ValidateNetestsInventory
    Scenario:
        Given A Nornir object based on an Ansible inventory
        Then This inventory is working

    Scenario:
        Given A Nornir object based on an Ansible with a connexion error
        Then This inventory is not working

    Scenario:
        Given A Nornir object based on an Ansible with a platform error
        Then This inventory is not working

    Scenario:
        Given A Nornir object based on an Ansible with a seucre_api error
        Then This inventory is not working

    Scenario:
        Given A Nornir object based on an Ansible with a port error
        Then This inventory is not working
