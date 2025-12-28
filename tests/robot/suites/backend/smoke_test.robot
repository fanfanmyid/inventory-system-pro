*** Settings ***
Resource          ../../resources/backend/auth_keywords.resource
Suite Setup       Setup API Session
Test Tags         smoke

*** Variables ***
${HEADERS}
${PRODUCT_ID}     1
${TEST_QTY}       2

*** Test Cases ***
Scenario 1: Authentication Health Check
    [Documentation]    Ensures the security layer (bcrypt/PASETO) is operational.
    ${token}=    Get Auth Token    ${USERNAME}    ${PASSWORD}
    Should Not Be Empty    ${token}
    ${headers}=    Create Dictionary    Authorization=Bearer ${token}    Content-Type=application/json
    Set Suite Variable    ${HEADERS}    ${headers}

Scenario 2: Product Data Availability
    [Documentation]    Verifies that the seed data exists in the database.
    ${resp}=    GET On Session    inventory    /api/v1/products/${PRODUCT_ID}    headers=${HEADERS}
    Status Should Be    200    ${resp}
    Dictionary Should Contain Key    ${resp.json()}    name
    Log    Product Name: ${resp.json()['name']}

Scenario 3: Transaction Logic (OUT)
    [Documentation]    Verifies that a basic Stock OUT transaction completes.
    ${payload}=    Create Dictionary    
    ...    product_id=${PRODUCT_ID}    
    ...    quantity=${TEST_QTY}    
    ...    transaction_type=OUT    
    ...    reference=SMOKE_TEST_OUT
    
    ${resp}=    POST On Session    inventory    /api/v1/transactions/    json=${payload}    headers=${HEADERS}
    Status Should Be    201    ${resp}

Scenario 4: Transaction Logic (IN)
    [Documentation]    Verifies that a basic Stock IN transaction completes.
    ${payload}=    Create Dictionary    
    ...    product_id=${PRODUCT_ID}    
    ...    quantity=${TEST_QTY}    
    ...    transaction_type=IN    
    ...    reference=SMOKE_TEST_IN
    
    ${resp}=    POST On Session    inventory    /api/v1/transactions/    json=${payload}    headers=${HEADERS}
    Status Should Be    201    ${resp}