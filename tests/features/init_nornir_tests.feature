# Created by dylan.hamel at 15.04.2020
Feature: Test init_nornir function
    # Description
    Scenario:
        Given I create a Nornir object with Ansible inventory in param
        Then There are 8 hosts in the inventory