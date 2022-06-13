$(() => {
    $('footer').hide();
    $(() => {
        const url = window.location.search;
        if (url.indexOf('preview=true') !== -1) {
            $('.negotiation-btn').hide();
        }
    });

    $('.carousel-item').first().addClass('active');
});