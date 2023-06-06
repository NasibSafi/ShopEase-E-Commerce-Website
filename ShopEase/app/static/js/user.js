$(function () {

    $('.oper_btn').each(function () {
        var status = $(this).attr('status')
        if (status == '4') {
            $(this).text('To evaluate')
        } else if (status == '5') {
            $(this).text('Completed')
        }
    })

    $('.oper_btn').on('click', function () {
        var trade_no = $(this).attr('trade_no')
        if ($(this).attr('status') == "1") {
            $.ajax({
                url: "/order/pay",
                method: "post",
                data: {
                    trade_no: trade_no,
                    csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()
                },
                success: function (data) {
                    if (data.res) {
                        window.open(data.msg)
                        $.ajax({
                            url: "/order/query",
                            method: "post",
                            data: {
                                trade_no: trade_no,
                                csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()
                            },
                            success: function (data) {
                                if (data.res) {
                                    alert('Payment successful')
                                    window.location.reload()
                                } else {
                                    alert('Payment failed')
                                }
                            }
                        })
                    } else {
                        alert(data.msg)
                    }
                }
            })
        } else if ($(this).attr('status') == '4') {
            window.location.href = '/order/comment/' + trade_no
        } else {
            alert("This order has been paid for")
        }
    })
})