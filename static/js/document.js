const log = function () {
    console.log.apply(console, arguments);
}

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

let imgItemTemplate = function (r) {
    let div = `
<div class="img-upload-item" data-name="${r.pic}">
    <img src="${r.pic}" alt="" class="img-user-pic-preview">
    <div class="right img-url-text">
        <div>${r.pic}</div>
        <a href="#" class="btn btn-danger btn-xs right btn-img-del">删除</a>
    </div>
</div>`
    return div
}

function Editor(input, preview) {
    this.update = function () {
        preview.innerHTML = markdown.toHTML(input.value);
    };
    input.editor = this;
    this.update();
}

function ajaxPicUpload() {
    let ajaxForm = $(event.target)
    ajaxForm.ajaxSubmit({
        success: function (message) {
            r = JSON.parse(message)
            if (r.status == 'success') {
                $('.img-upload-item-container').prepend(imgItemTemplate(r))
            }
            $('.alert-container').append(template(r))
            $('.alert').delay(2000).fadeOut(600)
        },
        error: function (data) {
            $('.alert-container').append(template({status: 'danger', msg: data.statusText}))
            $('.alert').delay(5000).fadeOut(600)
        },
        clearForm: true,
    });
    return false;
}

new Editor(document.getElementById("text-input"), document.getElementById("preview"));

$('.toggle-panel-heading').on('click', function (event) {
    let target = $(event.target)
    let panel = target.closest('.panel')
    let body = panel.find('.panel-body')
    body.slideToggle()
})

$('.img-upload-item-container').on('click', '.btn-img-del', function (event) {
    let target = $(event.target)
    let imgItem = target.closest('.img-upload-item')
    let imgName = imgItem.data('name')
    imgName = imgName.split('/').slice(-1)[0]
    let data = {
        'pic': imgName
    }
    let request = {
        url: '/user/pic/del',
        type: 'post',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function (r) {
            r = JSON.parse(r)
            if (r.status == 'success') {
                imgItem.remove()
                $('.alert-container').append(template(r))
                $('.alert').delay(2000).fadeOut(600)
            }
        },
        error: function (err) {
            log('error', err);
        }
    };
    $.ajax(request)
    return false
})