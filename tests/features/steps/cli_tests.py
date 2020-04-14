


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


@then(u'I can print help for select command')
def step_impl(context):
    pass


@then(u'I can print help for unselect command')
def step_impl(context):
    pass


@then(u'I can select * devices')
def step_impl(context):
    assert context.cli.check_input("select *")
    assert context.cli.select_action("select *")
    assert len(context.cli.devices) != 0


@then(u'I can unselect * devices')
def step_impl(context):
    assert context.cli.check_input("unselect *")
    assert context.cli.select_action("unselect *")
    assert len(context.cli.devices) == 0


@then(u'I can select only one devices')
def step_impl(context):
    assert context.cli.check_input("select leaf01")
    assert context.cli.select_action("select leaf01")
    assert len(context.cli.devices) != 0


@then(u'I can unselect only one devices')
def step_impl(context):
    assert context.cli.check_input("unselect leaf01")
    assert context.cli.select_action("unselect leaf01")
    assert len(context.cli.devices) == 0


@then(u'I can select many devices')
def step_impl(context):
    assert context.cli.check_input("select leaf01,leaf02")
    assert context.cli.select_action("select leaf01,leaf02")
    assert len(context.cli.devices) != 0

@then(u'I can unselect many devices')
def step_impl(context):
    assert context.cli.check_input("unselect leaf01,leaf02")
    assert context.cli.select_action("unselect leaf01,leaf02")
    assert len(context.cli.devices) == 0


@then(u'I can use selected command')
def step_impl(context):
    assert context.cli.check_input("selected")
    assert context.cli.select_action("selected")

@then(u'I can print help for print commands')
def step_impl(context):
    context.cli.print_print_help()


@then(u'I can print help for options commands')
def step_impl(context):
    context.cli.print_options_help()


@then(u'I can print * devices')
def step_impl(context):
    assert context.cli.check_input("print *")
    assert context.cli.select_action("print *")


@then(u'I can print only one devices')
def step_impl(context):
    assert context.cli.check_input("print leaf01")
    assert context.cli.select_action("print leaf01")


@then(u'I can print many devices')
def step_impl(context):
    assert context.cli.check_input("print leaf01,leaf02")
    assert context.cli.select_action("print leaf01,leaf02")





@then(u'I simulate a GET VRF command.')
def step_impl(context):
    assert context.cli.check_input("get vrf")








@then(u'I simulate a GET command without parameter.')
def step_impl(context):
    assert not(
        context.cli.check_input("get")
    )
