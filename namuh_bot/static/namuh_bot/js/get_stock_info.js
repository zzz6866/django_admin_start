"use strict";

document.addEventListener('DOMContentLoaded', () => {
    // const selector = document.getElementById('id_procorder_set-0-buy_cd');
    const selector = document.querySelector("#id_procorder_set-0-buy_cd");
    const link = document.createElement('a'); //<a href="javascript:;" onclick="getStockInfo()">종목 정보 조회</a>
    link.href = 'javascript:;';
    link.textContent = '종목 정보 조회';
    selector.appendChild(link);

});