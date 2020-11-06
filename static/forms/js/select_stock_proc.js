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
        $(document).on('change', 'select[id^=id_stockprocdtl_set-][id$=-cmd]', function (e) { // id_stockprocdtl_set-0-cmd
            const $row_index = $(this).attr('id').replace(/[^0-9]/g, "");
            const $this_value = $(this).val();
            const $this_value_level = $(this).children('option:selected').data('level');
            // console.log($row_index)
            // console.log($this_value)
            // console.log($this_value_level)
            $.each($('select[id^=id_stockprocdtl_set-' + $row_index + '-stockprocdtlval_set-][id$=-key]').children('option'), function (e){ // id_stockprocdtl_set-0-stockprocdtlval_set-0-key
                const $key_value_level = $(this).data('level');
                // console.log($key_value_level)
                if ($key_value_level === $this_value_level) {
                    $(this).show();
                } else {
                    $(this).hide();
                }

            });
        });

        $('select[id^=id_stockprocdtl_set-][id$=-cmd]').each(function (idx, e) {
            // console.log(idx);
            $(this).trigger('change', true)
        });
    });
}
