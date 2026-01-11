*** Settings ***
Library          SeleniumLibrary
Resource         ../../resources/frontend/locator.resource
Test Setup       Open Browser To Login Page
Test Teardown    Close Browser

*** Variables ***
${URL}           http://localhost:5173
${BROWSER}       chrome
${VALID_USER}    fanfanmyid
${VALID_PASS}    Sample123!

*** Test Cases ***
Scenario: Successful Login with Valid Credentials
    [Tags]    smoke    ui
    Input Text       ${LOGIN_USER_INPUT}    ${VALID_USER}
    Input Text       ${LOGIN_PASS_INPUT}    ${VALID_PASS}
    Click Button     ${LOGIN_SUBMIT_BTN}
    
    # Verify navigation to dashboard
    Wait Until Element Is Visible    ${DASHBOARD_BRAND}    timeout=10s
    Location Should Be               ${URL}/dashboard

Scenario: Failed Login with Invalid Credentials
    [Tags]    negative    ui
    Input Text       ${LOGIN_USER_INPUT}    wronguser
    Input Text       ${LOGIN_PASS_INPUT}    wrongpass
    Click Button     ${LOGIN_SUBMIT_BTN}
    
    # Verify error message is displayed
    Wait Until Element Is Visible    ${LOGIN_ERROR_MSG}    timeout=5s
    Element Should Contain           ${LOGIN_ERROR_MSG}    Invalid username or password

*** Keywords ***
Open Browser To Login Page
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Speed    0.5 seconds  # Slows down for demonstration