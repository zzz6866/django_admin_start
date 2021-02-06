'use strict';
const $ = jQuery;
$(document).ready(function () {
    $('#getStockInfo').on('click', function (e) {
        const buy_cd = $('#id_procorder_set-0-buy_cd').val();
        const login_id = $('#id_login_info').val();
        const elm = $(this);
        if (buy_cd && login_id) {
            const data_href_template = elm.attr('data-href-template').replace('__buy_cd__', buy_cd).replace('__login_id__', login_id);
            elm.attr('href', data_href_template);
        } else {
            if (!buy_cd) {
                alert("종목코드를 입력하세요.")
            }

            if (!login_id) {
                alert("증권사 아이디를 입력하세요.")
            }

            elm.removeAttr('href');
        }
    });
});
