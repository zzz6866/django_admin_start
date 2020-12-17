'use strict';
const $ = jQuery;
$(document).ready(function () {
    const buy_cd = $('#id_procorder_set-0-buy_cd')
    buy_cd.parent().append($('<a>', {href: 'javascript:;', onclick: 'getStockInfo(' + buy_cd.val() + ')', text: '종목 정보 조회', style: 'padding-left: 10px'}));
    buy_cd.parent().append($('<pre id="stock_info">'));

});

function getStockInfo(buy_cd) {
    $.ajax({
        url: '/namuh_bot/getStockinfoView/',
        type: 'POST',
        dataType: 'json',
        data: JSON.stringify({
            login_id: 1,
            buy_cd: buy_cd,
        }),
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", document.csrftoken);
        },
        success: function (data, textStatus, jqXHR) {
            $("#stock_info").text(JSON.stringify(data));
        }
    });
}

