*** Settings ***
Resource    ../../resources/backend/auth_keywords.resource
Suite Setup    Setup API Session

*** Variables ***
${HEADERS}
${PRODUCT_ID}
${SKU}

*** Test Cases ***
Scenario: Create Product with Random SKU
	[Tags]    feature    regression    product
	Given I am a logged in user
	When I create a product with random sku
	Then product creation should be successful
	And created product should be retrievable

Scenario: Update Product Price
	[Tags]    feature    regression    product
	Given I am a logged in user
	And I create a product with random sku
	When I update the product price to "25000"
	Then product update should be successful
	And product price should be "25000"

*** Keywords ***
I am a logged in user
	${token}=    Get Auth Token    ${USERNAME}    ${PASSWORD}
	${headers}=    Create Dictionary    Authorization=Bearer ${token}    Content-Type=application/json
	Set Suite Variable    ${HEADERS}    ${headers}

I create a product with random sku
	${random}=    Evaluate    __import__('random').randint(10000,99999)
	${sku}=    Set Variable    SKU-${random}
	${payload}=    Create Dictionary    sku=${sku}    name=QA Product ${random}    description=Auto test item    price=10000    stock=20
	${resp}=    POST On Session    inventory    /products/    json=${payload}    headers=${HEADERS}
	Set Suite Variable    ${LAST_RESP}    ${resp}
	Set Suite Variable    ${SKU}    ${sku}

product creation should be successful
	Status Should Be    200    ${LAST_RESP}
	${id}=    Get From Dictionary    ${LAST_RESP.json()}    id
	Set Suite Variable    ${PRODUCT_ID}    ${id}

created product should be retrievable
	${resp}=    GET On Session    inventory    /products/${PRODUCT_ID}    headers=${HEADERS}
	Status Should Be    200    ${resp}
	Should Be Equal As Strings    ${resp.json()['sku']}    ${SKU}

I update the product price to "${price}"
	${payload}=    Create Dictionary    price=${price}
	${resp}=    PATCH On Session    inventory    /products/${PRODUCT_ID}    json=${payload}    headers=${HEADERS}
	Set Suite Variable    ${LAST_RESP}    ${resp}

product update should be successful
	Status Should Be    200    ${LAST_RESP}

product price should be "${expected_price}"
	${resp}=    GET On Session    inventory    /products/${PRODUCT_ID}    headers=${HEADERS}
	Status Should Be    200    ${resp}
	${current_price}=    Convert To Number    ${resp.json()['price']}
	${expected_num}=    Convert To Number    ${expected_price}
	Should Be Equal As Numbers    ${current_price}    ${expected_num}
