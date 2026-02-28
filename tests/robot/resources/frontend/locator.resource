*** Variables ***
# Login Page IDs
${LOGIN_USER_INPUT}      id=input-username
${LOGIN_PASS_INPUT}      id=input-password
${LOGIN_SUBMIT_BTN}      id=btn-login-submit
${LOGIN_ERROR_MSG}       id=msg-login-error

# Dashboard IDs
${DASHBOARD_BRAND}       id=brand-logo
${LOGOUT_BTN}            id=btn-logout
${TABLE_INVENTORY}       id=table-inventory
${BTN_ADD_PRODUCT}       id=btn-add-product
${NAV_INVENTORY}         id=nav-inventory
${NAV_SALES}             id=nav-sales
${BTN_RESET_FILTERS}     id=btn-reset-filters
${BTN_REFRESH_HISTORY}   id=btn-refresh-history
${FILTER_NAME_INPUT}     id=filter-name
${FILTER_START_INPUT}    id=filter-start
${FILTER_END_INPUT}      id=filter-end
${FILTER_SIZE_SELECT}    id=filter-size
${TABLE_HISTORY}         id=table-history
${NO_HISTORY_ROW}        xpath=//table[@id='table-history']//td[contains(., 'No transactions')]
${BTN_UPDATE_STOCK}      xpath=(//button[@data-bs-target='#transactionModal'])[1]
${TX_MODAL}              id=transactionModal
${TX_TYPE_SELECT}        id=tx-type-select
${TX_QTY_INPUT}          id=tx-quantity-input
${TX_REF_INPUT}          id=tx-reference-input
${TX_SUBMIT_BTN}         id=tx-submit-btn
${TX_SUCCESS_MSG}        id=msg-success-tx

# Sales Page IDs
${BTN_NEW_SALE}          id=btn-open-sale-modal
${SALE_MODAL}            id=newSaleModal
${SALE_INVOICE_INPUT}    id=sale-invoice-input
${SALE_PRODUCT_SELECT}   id=sale-product-select-0
${SALE_QTY_INPUT}        id=sale-qty-input-0
${SALE_PRICE_INPUT}      id=sale-price-input-0
${BTN_SUBMIT_SALE}       id=btn-submit-sale
${SALE_SUCCESS_MSG}      id=msg-sale-success
${SALE_ERROR_MSG}        id=msg-sale-error
${TABLE_SALES}           id=table-sales
${SALES_NO_RECORDS}      xpath=//table[@id='table-sales']//td[contains(., 'No sales records')]