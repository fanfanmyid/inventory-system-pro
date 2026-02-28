*** Settings ***
Resource    ../../resources/backend/auth_keywords.resource
Suite Setup    Setup API Session

*** Variables ***
${HEADERS}
${PRODUCT_ID}
${START_STOCK}
${LAST_RESP}

*** Test Cases ***
Scenario: Perform Stock OUT (Reduction)
    [Tags]    regression    stock_out    transaction    feature
    Given I am a logged in user
    And I have a product with ID "1"
    When I perform a "OUT" transaction for "5" units
    Then the transaction should be successful
    And the product stock should be "decreased" by "5"

Scenario: Perform Stock IN (Restocking)
    [Tags]    regression    stock_in    transaction    feature
    Given I am a logged in user
    And I have a product with ID "1"
    When I perform a "IN" transaction for "10" units
    Then the transaction should be successful
    And the product stock should be "increased" by "10"

*** Keywords ***
I am a logged in user
    ${token}=    Get Auth Token    ${USERNAME}    ${PASSWORD}
    ${headers}=    Create Dictionary    Authorization=Bearer ${token}    Content-Type=application/json
    Set Suite Variable    ${HEADERS}    ${headers}

I have a product with ID "${id}"
    ${resp}=    GET On Session    inventory    /products/${id}    headers=${HEADERS}
    Status Should Be    200    ${resp}
    ${current_stock}=    Convert To Integer    ${resp.json()['stock']}
    Set Suite Variable    ${PRODUCT_ID}    ${id}
    Set Suite Variable    ${START_STOCK}   ${current_stock}

I perform a "${type}" transaction for "${quantity}" units
    [Documentation]    Matches documentation: product_id, quantity, transaction_type, reference.
    ${qty_int}=    Convert To Integer    ${quantity}
    ${payload}=    Create Dictionary    
    ...    product_id=${PRODUCT_ID}    
    ...    quantity=${qty_int}    
    ...    transaction_type=${type}    
    ...    reference=QA_AUTO_REF_${type}
    
    ${resp}=    POST On Session    inventory    /transactions/    json=${payload}    headers=${HEADERS}
    Set Suite Variable    ${LAST_RESP}    ${resp}

the transaction should be successful
    Status Should Be    200   ${LAST_RESP}

the product stock should be "${direction}" by "${amount}"
    [Documentation]    Calculates expected stock based on IN (addition) or OUT (subtraction).
    ${resp}=    GET On Session    inventory    /products/${PRODUCT_ID}    headers=${HEADERS}
    ${final_stock}=    Convert To Integer    ${resp.json()['stock']}
    ${change}=         Convert To Integer    ${amount}
    
    # Dynamic Math Calculation
    ${expected}=    Run Keyword If    '${direction}' == 'increased'    Evaluate    ${START_STOCK} + ${change}
    ...    ELSE IF    '${direction}' == 'decreased'    Evaluate    ${START_STOCK} - ${change}
    
    Should Be Equal As Integers    ${final_stock}    ${expected}