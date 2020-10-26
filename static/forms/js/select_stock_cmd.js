/*
(function() {
    $('select[id^=id_stockprocdtl_set-][id$=-cmd]').on("change", function (e) {
        // const row_index = $(this).attr('id').replace(/[^0-9]/g, "");
        console.log(e)
        console.log(row_index)
    });
    console.log($.each(function (i,e) {
        alert("Asd")
    }))
})*/
'use strict';
{
    const $ = django.jQuery;
    $(document).ready(function () {
       console.log('sdfsdfsdf');
       $('#stockprocdtl_set-0-cmd').change(function (e) {
           console.log("1234");
       });
    });
}
