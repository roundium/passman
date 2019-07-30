;(function ($) {
    $(document).ready(function () {
        let imgNode = document.createElement('img');
        imgNode.setAttribute('src', '/static/img/eye-regular.svg');
        imgNode.setAttribute('alt', 'show-password');
        imgNode.classList.add('show-password');

        let referenceNode = document.querySelector('#id_password');
        referenceNode.setAttribute('type', 'password');
        referenceNode.after(imgNode);

        $('img.show-password').click(function () {
            if (referenceNode.getAttribute('type') === 'password') {
                referenceNode.setAttribute('type', 'text');
                imgNode.setAttribute('src', '/static/img/eye-slash-regular.svg');
            } else {
                referenceNode.setAttribute('type', 'password');
                imgNode.setAttribute('src', '/static/img/eye-regular.svg');
            }
        });
    });
})($);
