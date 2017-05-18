// $('#id-button-verify').click(function(event) {
//     let mailCodeButton = $(event.target)
//     let form = mailCodeButton.closest('form')
//     console.log(form)
//     t = 60
//     mailCodeButton.text(`获取验证邮件（ ${t} ）`)
//     mailCodeButton.attr('disabled', true)
//     let timer = setInterval(function() {
//         t -= 1
//         mailCodeButton.text(`获取验证邮件（ ${t} ）`)
//         if (t <= 0) {
//             clearInterval(timer)
//             mailCodeButton.removeAttr('disabled')
//             mailCodeButton.text(`获取验证邮件`)
//         }
//     }, 1000);
//     return false
// })
let template = function (r) {
    let div = `
<div class="alert alert-${r.status} alert-dismissible" role="alert" >
    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">×</span>
    </button>
    ${r.msg}
</div>`
    return div
}

$('.button-re-verify').click(function() {
    $('#id-div-email-info').toggle()
    $('#id-div-email-update').toggle()
})

let ajaxFormSubmit = function() {
    let ajaxForm = $(event.target)
    let img = ajaxForm.find('img')
    img.click()
    let mailCodeButton = ajaxForm.find('#id-button-verify')
    let alertContainer = $('.alert-container')
    ajaxForm.ajaxSubmit(function(response) {
        let r = JSON.parse(response)
        alertContainer.append(template(r))
        $('.alert').delay(5000).fadeOut(600)

    });
    let t = 60
    mailCodeButton.text(`获取验证邮件（ ${t} ）`)
    mailCodeButton.attr('disabled', true)
    let timer = setInterval(function() {
        t -= 1
        mailCodeButton.text(`获取验证邮件（ ${t} ）`)
        if (t <= 0) {
            clearInterval(timer)
            mailCodeButton.removeAttr('disabled')
            mailCodeButton.text(`获取验证邮件`)
        }
    }, 1000);
    return false;
}
