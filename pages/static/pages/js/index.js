$(() => {
    $('.navbar .navbar-toggler').on('click', ev => {
        $('.navbar').toggleClass('menu-expanded');
    });
    $('.navbar .nav-item').on('click', ev => {
        const navbar = $('.navbar');
        if (navbar.hasClass('menu-expanded')) {
            $('.navbar .navbar-toggler').trigger('click');
        } 
    });
    let film_roll = new FilmRoll({
        container: '#film-roll',
    });
    setTimeout(() => film_roll.resize(), 100);

    $('div.home-box > div.product-image').on('click', (ev) => {
        let box = $(ev.target);
        if (!box.hasClass('product-image')) {
            box = box.parent();
        }
        console.log(box);
        const group = box.attr('data-group');
        const filter = box.attr('data-filter');
        const filterby = box.attr('data-filterby');
        console.log(filter);
        const url = `/products/offers/${group}/${filterby}/${filter}/`;
        location.assign(url);
    });



});