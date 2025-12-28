*** Settings ***
Resource    ../../resources/backend/auth_keywords.resource
Suite Setup    Setup API Session

*** Variables ***
${token}
${headers}
${initial_stock}

*** Test Cases ***
Scenario: User Should Be Able To Checkout Successfully
    [Documentation]    E2E flow for purchasing a product.
    [Tags]    regression    sales
    Given Login with PASETO TOKEN    ${USERNAME}    ${PASSWORD}
    When Initial Body Request
    And Hit Api sales
    Then Verify Data and Stock Reduction

*** Keywords ***
Login with PASETO TOKEN
    [Arguments]    ${username}    ${password}
    ${token}=    Get Auth Token    ${username}    ${password}
    Set Test Variable   ${token}

    
Initial Body Request
    ${headers}=    Create Dictionary    Authorization=Bearer ${token}
    ${resp}=    GET On Session    inventory    /products/1    headers=${headers}
    ${initial_stock}=    Convert To Integer    ${resp.json()}[stock]
    Set Test Variable    ${initial_stock}
    Set Test Variable    ${headers}

Hit Api sales
    ${item}=    Create Dictionary    product_id=1    quantity=2
    ${items}=    Create List    ${item}
    ${payload}=    Create Dictionary    items=${items}
    ${resp}=    POST On Session    inventory    /sales/    json=${payload}    headers=${headers}
    Status Should Be    200    ${resp}

Verify Data and Stock Reduction
    ${resp}=    GET On Session    inventory    /products/1    headers=${headers}
    ${new_stock}=    Set Variable    ${resp.json()['stock']}
    ${expected_stock}=    Evaluate    int(${initial_stock})-2
    Should Be Equal As Integers    ${new_stock}    ${expected_stock}