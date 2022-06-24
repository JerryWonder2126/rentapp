$(() => {
    $('.navbar .navbar-toggler').on('click', ev => {
        // To add class to menu - class is only active on small devices
        $('.navbar').toggleClass('menu-expanded');
    });
    $('.navbar .nav-item').on('click', ev => {
        // Simply to handle toggling of mennu-expanded class on menu
        const navbar = $('.navbar');
        const objClicked = $(ev.target);
        if (navbar.hasClass('menu-expanded') && !objClicked.hasClass('dropdown-toggle')) {
            // Second condition is to prevent toggling class when menu dropdown link is pressed
            $('.navbar .navbar-toggler').trigger('click');
        } 
    });
    // let film_roll = new FilmRoll({
    //     container: '#film-roll',
    // });
    // setTimeout(() => film_roll.resize(), 100);

    $('div.home-box > div.product-image').on('click', (ev) => {
        let box = $(ev.target);
        if (!box.hasClass('product-image')) {
            box = box.parent();
        }
        const group = box.attr('data-group');
        const filter = box.attr('data-filter');
        const filterby = box.attr('data-filterby');
        const url = `/products/offers/${group}/${filterby}/${filter}/`;
        location.assign(url);
    });

    backOneStep = () => window.history.back();  // To go back to previous page

    // FOR FAQs PAGE
    $(".faq-card .card-body").toggle(); // Hide answers to faqs by default

    $('.toggle-btn').on('click', (ev) => {
        // Toggle faqs answers on btn click
        const btn = $(ev.target);
        if (btn.hasClass('toggled')) {
            btn.removeClass('toggled');
            btn.text('+');
        } else {
            btn.addClass('toggled');
            btn.text('-');
        }
        const answer = btn.parents('div.faq-card').find('div.card-body');
        answer.toggle();
    });
    // END OF FOR FAQs PAGE

    $(() => {   // Loads tags attached to homes dynamically into dom for /home route
        let tagsDiv = $(".home-tags");
        $.each(tagsDiv, function (index, tagDiv) { 
            let tags = $(tagDiv).attr('data-tags');
            if (tags) {
                let tagsList = tags.split(', ');
                $.each(tagsList, function (index, tag) { 
                    $(tagDiv).append(`<span class="home-tag ${tag}">${tag}</span>`);
                }); 
            }
        });
    });

});