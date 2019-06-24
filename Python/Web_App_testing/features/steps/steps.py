import re
from behave import *
from time import sleep
from strgen import StringGenerator

use_step_matcher("parse")


# <editor-fold desc="Basic Steps for Web base Apps">
@step("I go to {page_url}")
def step_impl(context, page_url):
    """
    :param page_url: Page url that we will be opening.
    :type context: behave.runner.Context
    """
    # This will allows to use the same step for one use URL as well as urls in the Config.yaml file.
    try:
        context.browser.goto(context.data[page_url])
        print(f'Opening {context.data[page_url]}\n')
    except KeyError:
        context.browser.goto(page_url)
        print(f'Opening {page_url}\n')


@step("I close the Browser")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.browser.close()


@step("I clear the Browser's cookies")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.browser.cookies.clear()


@step("The page title should be {title}")
def step_impl(context, title):
    """
    :param title: str, Expected page title
    :type context: behave.runner.Context
    """
    sleep(1)
    assert title in context.browser.title.strip(), f"Current Page Title: {context.browser.title}\n" \
        f"Expected Page Title: {title}\n"
    print(f'The Current Page Title: {context.browser.title} matches the '
          f'Expected Page Title: {title}\n')


@step("Click on browser back button")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.browser.back()
    sleep(1)


@step("I check {message} is present in the page")
def step_impl(context, message):
    """
    :param message: Message/text to search for in the page.
    :type context: behave.runner.Context
    """
    if message in context.fake_user:
        assert context.fake_user[message] in context.browser.html, f"Couldn't find {context.fake_user[message]}" \
            f" in the Web page.\n"
        print(f'{context.fake_user[message]} is present in the page.\n')
    else:
        assert str(message) in context.browser.html, f"Couldn't find {message} in the Web page.\n"
        print(f'The message "{message}" is present in the page.\n')


@step("Verified {message} is in the URL")
def step_impl(context, message):
    """
    :param message: String to search for in the URL
    :type context: behave.runner.Context
    """

    assert message in context.browser.url, f"Couldn't find {message} in {context.browser.url}.\n"
    print(f'{message} is present in the url.\n')


@step("I switch tabs")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.browser.windows()[1].use()


@step("I close the tab")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    print(f'Closing the tab {context.browser.url}')
    context.browser.windows()[1].close()
    context.browser.windows()[0].use()
    print(f'Returning to {context.browser.title}\n')


@step("I Wait")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    sleep(100)


# </editor-fold>


@step("Login using the credentials for {user}")
def step_impl(context, user):
    """
    :param user: str, To use when login in.
    :type context: behave.runner.Context
    """
    # Login page objects
    print(f'We Login using the stored credentials for {user}.\n')
    context.browser.text_field(id='username').clear()
    context.browser.text_field(id='username').send_keys(context.data[user]["username"])
    context.browser.text_field(id='password').clear()
    context.browser.text_field(id='password').send_keys(context.data[user]['password'])
    context.browser.input(value='Sign In').click()


@step("I click the {html_tag} with {selector}={identifier}")
def step_impl(context, html_tag, selector, identifier):
    """
    This step is sorta of a catch all for all basic clicks.
    :param selector: text, id, name, etc.
    :param identifier: text, id, or name, depends on the tag you provide.
    :param html_tag: a, input, button, etc. i'll update this as we add them.
    :type context: behave.runner.Context
    """
    context.browser.wait()
    # ADD a dict to make finding objects more dynamic
    kwargs = {selector.lower(): identifier}
    if html_tag.lower() == 'link' or html_tag.lower() == 'a':
        context.browser.link(kwargs).click()
    elif html_tag.lower() == 'input':
        context.browser.input(kwargs).js_click()
    elif html_tag.lower() == 'button':
        context.browser.button(kwargs).click()
    elif html_tag.lower() == 'image':
        context.browser.image(kwargs).click()
    else:
        assert False, f"No method to handle elements of tag {html_tag}"
    print(f'We click on {identifier}\n')


@step("I type {payload} in the field with {identifier}-{value}")
def step_impl(context, payload, identifier, value):
    """
    This step will handle all the typing, should work as long as the html tag is of type input.
    :param payload: What to type, you can also have it create it for you using the random options.
    :param identifier: Type of identifiers. Ex: ID or name.(This will be the only 2 we will support)
    :param value: of the Identifier.
    :type context: behave.runner.Context
    """
    kwargs = {identifier.lower(): value}
    if "random" in payload.lower():
        payload = payload.replace('Random ', '')
        if payload == 'First Name':
            context.browser.input(kwargs).send_keys(context.fake.last_name().capitalize())
        elif payload == 'Last Name':
            context.browser.input(kwargs).send_keys(context.fake.first_name().capitalize())
        elif payload == 'Email':
            context.browser.input(kwargs).send_keys(context.fake.email())
        elif payload == 'Password':
            context.browser.input(kwargs).send_keys(
                StringGenerator(r'[\c]{4:8}&[!#\$]&[\d]&[\u]{2}').render())
        elif payload == 'Username':
            context.browser.input(kwargs).send_keys(context.fake.name().replace(" ", "").lower())
        # This will store this for future uses during the application
        context.fake_user[payload] = context.browser.text_field(kwargs).value
        print(f"{payload} set to {context.fake_user[payload]}\n")
    elif "previous" in payload.lower():
        payload = payload.replace('Previous ', '')
        context.browser.input(kwargs).send_keys(context.fake_user[payload])
        print(f"{payload} set to {context.fake_user[payload]}\n")
    elif "temporary" in payload.lower():
        payload = payload.replace('Temporary ', '')
        if payload == 'Email':
            context.fake_user[payload] = context.temp_email
            context.browser.input(kwargs).send_keys(context.fake_user[payload])
            print(f"{payload} set to {context.fake_user[payload]}\n")
    else:
        context.browser.input(kwargs).send_keys(payload)


@step("I validate that the {html_tag} with {selector}={identifier} has an attribute {name}={value}")
def step_impl(context, html_tag, selector, identifier, name, value):
    """
    This steps allows us to check on attributes in the html code.
    :param html_tag: input, button, etc... (if not set below, please add it)
    :param selector: ID, name, value, etc...
    :param identifier: value of the selector.
    :param name: name of the attribute we are going to check on.
    :param value: expected value in the attribute we pass in the name var.
    :type context: behave.runner.Context
    """
    # ADD a dict to make finding objects more dynamic
    kwargs = {selector.lower(): identifier}
    if html_tag.lower() == 'link' or html_tag.lower() == 'a':
        current_value = context.browser.link(kwargs).get_attribute(name)
    elif html_tag.lower() == 'input':
        current_value = context.browser.input(kwargs).get_attribute(name)
    elif html_tag.lower() == 'image':
        current_value = context.browser.image(kwargs).get_attribute(name)
    elif html_tag.lower() == 'paragraph':
        current_value = context.browser.p(kwargs).get_attribute(name)
    else:
        assert False, f"No method to handle elements of tag {html_tag}"
    assert str(current_value) in str(value), f"The current value of {name} is {current_value}, " \
        f"not {value}"
    print(f'The Field {identifier} has an attribute {name} with the value of {current_value} \n')


@step("I validate that the {html_tag} with {selector}={identifier} contains the text {value}")
def step_impl(context, html_tag, selector, identifier, value):
    """
    This steps allows us to check on Text contained.
    :param html_tag: input, button, etc... (if not set below, please add it)
    :param selector: ID, name, value, etc...
    :param identifier: value of the selector.
    :param value: expected Expected text in the element.
    :type context: behave.runner.Context
    """
    # ADD a dict to make finding objects more dynamic
    kwargs = {selector.lower(): identifier}
    if html_tag.lower() == 'link' or html_tag.lower() == 'a':
        current_value = context.browser.link(kwargs).text
    elif html_tag.lower() == 'input':
        current_value = context.browser.input(kwargs).text
    elif html_tag.lower() == 'span':
        current_value = context.browser.span(kwargs).text
    elif html_tag.lower() == 'paragraph':
        sleep(3)
        current_value = context.browser.p(kwargs).text
    else:
        assert False, f"No method to handle elements of tag {html_tag}"
    assert str(current_value) == str(value), f"The current text of {identifier} is {current_value}, " \
        f"not {value}"
    print(f'The Text for {identifier} matches the expected {current_value} \n')


@step("I check my email for the Email Verification Link")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    found = False
    while not found:
        for x in iter(context.email_session.get_email_list()):
            if context.email_session.get_email(x.guid).subject == "Verify email":
                pattern = re.compile('"([^"]*)"')
                context.data['MSD Email Verification'] = \
                    pattern.findall(str(context.email_session.get_email(x.guid).body))[0]
                found = True
                break
        sleep(5)
    context.clean_kc = True

@step("I validate that the image with {selector}={identifier} has loaded correctly")
def step_impl(context, selector, identifier):
    """
    This is used to validate has loaded correct, the way we achieve this is by testing the width of the picture,
    if it's equal to 0 then we will assume it failed to load properly.
    :param selector: ID, name, value, etc...
    :param identifier: value of the selector.
    :type context: behave.runner.Context
    """
    kwargs = {selector.lower(): identifier}
    assert context.browser.image(
        kwargs).loaded is True, f"The image with {selector}={identifier} didn't load correctly!\n"
    print(f"The image with {selector}={identifier} loaded correctly!\n")


@given("I create a temporary account")
def step_impl(context):
    """
    This step will create a new account using a Guerrilla email and verify the email.
    :type context: behave.runner.Context
    """
    context.execute_steps(u'''
                        given I go to MSD
                        then I click the Link with text=Register
                        and I type Random First Name in the field with ID-firstName
                        and I type Random Last Name in the field with ID-lastName
                        and I type Temporary Email in the field with ID-email
                        and I type Random Username in the field with ID-username
                        and I type Random Password in the field with ID-password
                        and I type Previous Password in the field with ID-password-confirm
                        then I click the Input with value=Register
                        and I check my email for the Email Verification Link
                        and I go to MSD Email Verification
                        and I validate that the Paragraph with Class=App-Title contains the text All Applications
                        and I clear the Browser's cookies
            ''')


@step("I check my email for the Reset Password")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    found = False
    while not found:
        for x in iter(context.email_session.get_email_list()):
            if context.email_session.get_email(x.guid).subject == "Reset Password":
                pattern = re.compile('"([^"]*)"')
                context.data['MSD Forgot Password'] = \
                    pattern.findall(str(context.email_session.get_email(x.guid).body))[0]
                found = True
                break
        sleep(5)


@step("I validate that the Dropbox with {selector}={identifier} contains the options in this list")
def step_impl(context, selector, identifier):
    """
    :param selector: ID, name, value, etc...
    :param identifier: value of the selector.
    :type context: behave.runner.Context
    """
    sleep(3)
    kwargs = {selector.lower(): identifier}
    context.browser.wait()
    options = context.browser.select(kwargs)
    for row in context.table:
        assert options.includes(row[0]), f'The option "{row[0]}" ' \
            f'is not present in the Dropbox with {selector}={identifier}'
        print(f'The Option {row[0]} is present in the Dropbox with {selector}={identifier}')


@step("I check my inbox for {email_num} Invalid User Name or Password email(s)")
def step_impl(context, email_num):
    """
    :param email_num: Number of times i should have the email in my inbox
    :type context: behave.runner.Context
    """
    found = 0
    while int(found) != int(email_num):
        found = 0
        for x in iter(context.email_session.get_email_list()):
            sleep(3)
            if context.email_session.get_email(x.guid).subject == "Invalid User Name or Password":
                found += 1
        sleep(6)
    assert str(found) == str(email_num), f'The number of matches in the inbox is not the expected!'
    print(f'There is {found} emails for invalid logins in the Inbox as expected!\n')