*** Settings ***
Library    RequestsLibrary
Library    Collections
Variables    variables.py


*** Keywords ***
Get Auth Token
    [Arguments]    ${username}    ${password}
    ${auth_data}=    Create Dictionary    username=${username}    password=${password}
    ${resp}=    POST On Session    inventory    /auth/login    data=${auth_data}
    Status Should Be    200    ${resp}
    ${token}=    Get From Dictionary    ${resp.json()}    access_token
    RETURN    ${token}

Setup API Session
    Create Session    inventory    ${BASE_URL}    verify=True