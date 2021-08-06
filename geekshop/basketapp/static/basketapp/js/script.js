window.onload = function () {
    const inp = $('.basket_list')

    function change_inp (t_href, current) {
        $.ajax({
            url: "/basket/edit/" + t_href.name + "/" + t_href.value + "/",
            success: function (data) {
                if (t_href.value > 0) {
                    $('.basket_summary').replaceWith(data.result);
                    current.parent().next().text(data.product_price + ' руб.');
                } else {
                    current.parent().parent().detach();
                }
            },
        });
    };

    inp.on('input', 'input[type=number]', function (event) {
        change_inp(event.target, $(this));
    });
}