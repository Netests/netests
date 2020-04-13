


from functions.base_cli import NetestsCLI


@given(u'I create a NetestsCLI object with Ansible parameters named cli')
def step_impl(context):
    context.cli = NetestsCLI(
        ansible=True
    )


@given(u'I print NetestsCLI object')
def step_impl(context):
    print(context.cli)








@then(u'I can print help')
def step_impl(context):
    context.cli.print_help()


@then(u'I can print help for options commands')
def step_impl(context):
    context.cli.print_options_help()





@then(u'I simulate a GET VRF command.')
def step_impl(context):
    print(context.cli.check_input("get vrf"))
    assert context.cli.check_input("get vrf")








@then(u'I simulate a GET command without parameter.')
def step_impl(context):
    assert not(
        context.cli.check_input("get")
    )
