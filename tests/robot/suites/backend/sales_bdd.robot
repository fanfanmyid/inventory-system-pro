*** Settings ***
Resource    ../../resources/backend/auth_keywords.resource
Suite Setup    Setup API Session

*** Variables ***
${HEADERS}
${PRODUCT_ID}
${START_STOCK}
${LAST_RESP}
${QTY_SOLD}

*** Test Cases ***
Scenario: User performs a checkout with dynamic stock verification
    [Tags]    feature    regression    sales
    Given I am a logged in user
    And I have a product with ID "1"
    When I checkout "2" units of that product
    Then the checkout should be successful
    And the product stock should be updated correctly

*** Keywords ***
I am a logged in user
    ${token}=    Get Auth Token    ${USERNAME}    ${PASSWORD}
    ${headers}=    Create Dictionary    Authorization=Bearer ${token}
    Set Suite Variable    ${HEADERS}    ${headers}

I have a product with ID "${id}"
    ${resp}=    GET On Session    inventory    /products/${id}    headers=${HEADERS}
    Status Should Be    200    ${resp}
    
    # Capture the REAL current stock from the response
    ${current_actual_stock}=    Convert To Integer    ${resp.json()['stock']}
    
    # Store these as Suite Variables so other keywords can see them
    Set Suite Variable    ${PRODUCT_ID}    ${id}
    Set Suite Variable    ${START_STOCK}    ${current_actual_stock}

I checkout "${quantity}" units of that product
    ${qty}=    Convert To Integer    ${quantity}
    ${unit_price}=    Set Variable    1000000
    ${item}=    Create Dictionary    product_id=${PRODUCT_ID}    quantity=${qty}    unit_price=${unit_price}
    ${items}=    Create List    ${item}
    ${total_price}=    Evaluate    ${qty} * ${unit_price}
    ${payload}=    Create Dictionary    items=${items}    total_price=${total_price}
    ${random}=    Evaluate    __import__('random').randint(10000,99999)
    ${invoice_number}=    Set Variable    INV-${random}
    Set To Dictionary    ${payload}    invoice_number=${invoice_number}
    
    ${resp}=    POST On Session    inventory    /sales/    json=${payload}    headers=${HEADERS}
    
    # Store the quantity sold to calculate the math later
    Set Suite Variable    ${QTY_SOLD}    ${qty}
    Set Suite Variable    ${LAST_RESP}    ${resp}

the checkout should be successful
    Status Should Be    200    ${LAST_RESP}

the product stock should be updated correctly
    ${resp}=    GET On Session    inventory    /products/${PRODUCT_ID}    headers=${HEADERS}
    ${final_stock}=    Convert To Integer    ${resp.json()['stock']}
    
    # Dynamic Math: Initial (Live) Stock - Quantity Sold
    ${expected}=    Evaluate    ${START_STOCK} - ${QTY_SOLD}
    
    Should Be Equal As Integers    ${final_stock}    ${expected}