*** Settings ***
Library          SeleniumLibrary
Resource         ../../resources/frontend/locator.resource
Suite Setup      Open Browser Session
Suite Teardown   Close Browser
Test Setup       Ensure Dashboard Session

*** Variables ***
${URL}           http://localhost:5173
${BROWSER}       chrome
${VALID_USER}    fanfanmyid
${VALID_PASS}    Sample123!

*** Test Cases ***
Scenario: Inventory table loads after login
    [Tags]    regression    ui    inventory
    Wait Until Element Is Visible    ${TABLE_INVENTORY}    10s
    ${row_count}=    Get Element Count    xpath=//table[@id='table-inventory']/tbody/tr
    Should Be True    ${row_count} > 0    msg=Inventory table should show at least one product row.

Scenario: Filtering transactions shows empty state for unmatched criteria
    [Tags]    feature    ui    transactions
    Clear Element Text    ${FILTER_NAME_INPUT}
    ${random}=    Evaluate    __import__('uuid').uuid4().hex
    Input Text    ${FILTER_NAME_INPUT}    ${random}
    Click Button    ${BTN_REFRESH_HISTORY}
    Wait Until Element Is Visible    ${NO_HISTORY_ROW}    10s
    Click Button    ${BTN_RESET_FILTERS}

Scenario: Update stock via dashboard modal
    [Tags]    regression    ui    inventory
    Click Button    ${BTN_UPDATE_STOCK}
    Wait Until Element Is Visible    ${TX_MODAL}    5s
    Select From List By Value    ${TX_TYPE_SELECT}    IN
    Clear Element Text    ${TX_QTY_INPUT}
    Input Text    ${TX_QTY_INPUT}    1
    Input Text    ${TX_REF_INPUT}    UI Restock
    Click Button    ${TX_SUBMIT_BTN}
    Wait Until Element Is Visible    ${TX_SUCCESS_MSG}    10s

Scenario: User can logout from dashboard
    [Tags]    smoke    ui    auth
    Click Button    ${LOGOUT_BTN}
    Wait Until Element Is Visible    ${LOGIN_USER_INPUT}    10s
    Location Should Contain    ${URL}

*** Keywords ***
Open Browser Session
    Open Browser    about:blank    ${BROWSER}
    Maximize Browser Window

Ensure Dashboard Session
    ${is_dashboard}=    Run Keyword And Return Status    Page Should Contain Element    ${DASHBOARD_BRAND}
    IF    not ${is_dashboard}
        Login Through UI
    END

Login Through UI
    Go To    ${URL}
    Wait Until Element Is Visible    ${LOGIN_USER_INPUT}    10s
    Input Text    ${LOGIN_USER_INPUT}    ${VALID_USER}
    Input Text    ${LOGIN_PASS_INPUT}    ${VALID_PASS}
    Click Button   ${LOGIN_SUBMIT_BTN}
    Wait Until Element Is Visible    ${DASHBOARD_BRAND}    15s
    Wait Until Element Is Visible    ${TABLE_INVENTORY}    15s
