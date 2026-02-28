*** Settings ***
Library          SeleniumLibrary
Resource         ../../resources/frontend/locator.resource
Suite Setup      Open Browser Session
Suite Teardown   Close Browser
Test Setup       Ensure Sales Session

*** Variables ***
${URL}           http://localhost:5173
${BROWSER}       chrome
${VALID_USER}    fanfanmyid
${VALID_PASS}    Sample123!

*** Test Cases ***
Scenario: Sales history table is visible
    [Tags]    regression    ui    sales
    Wait Until Element Is Visible    ${TABLE_SALES}    15s
    ${rows}=    Get Element Count    xpath=//table[@id='table-sales']/tbody/tr
    Should Be True    ${rows} >= 1    msg=Sales history should display at least one row (or placeholder row).

Scenario: User records a sale via modal
    [Tags]    feature    ui    sales
    Click Button    ${BTN_NEW_SALE}
    Wait Until Element Is Visible    ${SALE_MODAL}    10s
    Wait Until Element Is Visible    ${SALE_PRODUCT_SELECT}    10s
    Select From List By Index    ${SALE_PRODUCT_SELECT}    1
    Clear Element Text    ${SALE_QTY_INPUT}
    Input Text    ${SALE_QTY_INPUT}    1
    Clear Element Text    ${SALE_PRICE_INPUT}
    Input Text    ${SALE_PRICE_INPUT}    50000
    Click Button    ${BTN_SUBMIT_SALE}
    Wait Until Element Is Visible    ${SALE_SUCCESS_MSG}    10s

*** Keywords ***
Open Browser Session
    Open Browser    about:blank    ${BROWSER}
    Maximize Browser Window

Ensure Sales Session
    ${on_sales}=    Run Keyword And Return Status    Page Should Contain Element    ${TABLE_SALES}
    IF    not ${on_sales}
        Login And Navigate To Sales
    END

Login And Navigate To Sales
    Go To    ${URL}
    Wait Until Element Is Visible    ${LOGIN_USER_INPUT}    15s
    Input Text    ${LOGIN_USER_INPUT}    ${VALID_USER}
    Input Text    ${LOGIN_PASS_INPUT}    ${VALID_PASS}
    Click Button   ${LOGIN_SUBMIT_BTN}
    Wait Until Element Is Visible    ${DASHBOARD_BRAND}    15s
    Click Element    ${NAV_SALES}
    Wait Until Element Is Visible    ${TABLE_SALES}    15s
