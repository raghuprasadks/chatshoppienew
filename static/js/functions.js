(function ($) {
    // maga menu
    var megaMenuOpen = function () {
        $('.dropdown-menu', this).not('.in .dropdown-menu').stop(true, true).slideDown("200");
        $(this).toggleClass('open');
    };
    var megaMenuClose = function () {
        $('.dropdown-menu', this).not('.in .dropdown-menu').stop(true, true).slideUp("200");
        $(this).toggleClass('open');
    };
    var windowWidth = $(window).width();
    if(windowWidth > 768 ) {
        $(".navbar-default .navbar-nav li.dropdown").hover(megaMenuOpen,megaMenuClose);
    }


    $(".clients-carousel").owlCarousel({
        responsive : {
            0 : { items : 2  },
            500 : { items : 3  },
            700 : { items : 4  },
            1199 : { items : 5  }
        },
        items:5,
        margin:20
    });

    $(".works-carousel").owlCarousel({
        responsive : {
            0 : { items : 1  },
            500 : { items : 2  },
            991 : { items : 3  }
        },
        items: 3,
        nav: true,
        dots: false,
        navText: ['', ''],
        margin:20
    });

    $(".basic-testimonial-carousel").owlCarousel({
        items: 1,
        margin:20
    });

    $(".classic-testimonial-carousel").owlCarousel({
        items: 1,
        nav: true,
        dots: false,
        margin:20,
        navText: ['', '']
    });

    $(".testimonial-carousel").owlCarousel({
        responsive : {
            0 : { items : 1  }, // from zero to 480 screen width 4 items
            1000 : { items : 2  } // from zero to 480 screen width 4 items
        },
        items: 2,
        slideBy: 2,
        margin:20
    });

    $(".chat-testimonial-carousel").owlCarousel({
        responsive : {
            0 : { items : 1  }, // from zero to 480 screen width 4 items
            1000 : { items : 2  } // from zero to 480 screen width 4 items
        },
        items: 2,
        slideBy: 2,
        margin:20
    });

    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    });

    // hide our element on page load
    $('.animation').css('opacity', 0);

    $('.animation').waypoint(function() {
        $(this.element).addClass('animated').css('opacity', 1);
    }, { offset: '90%' });

    $(function () {
        $('[data-toggle="popover"]').popover()
    });

    $("a.menu-icon").click(function () {
        $(".menu-backdrop").toggle();
        $(".menu-backdrop").toggleClass("in");
    });

    $(".menu-backdrop").click(function () {
        $(".menu-backdrop").toggle();
        $(".menu-backdrop").toggleClass("in");
    });

    $(".mobile-menu-icon").click(function (event) {
        event.preventDefault();
    });

    if($(this).length) {
        $('#side-nav').metisMenu();
    }

    var $window = $(window), $container = $('div.page-container');

    $('body').on('click', '.panel > .panel-heading > .panel-tool-options li > a[data-rel="reload"]', function (ev) {
        ev.preventDefault();

        var $this = $(this).closest('.panel');

        $this.block({
            message: '',
            css: {
                border: 'none',
                padding: '15px',
                backgroundColor: '#fff',
                '-webkit-border-radius': '10px',
                '-moz-border-radius': '10px',
                opacity: .5,
                color: '#fff',
                width: '50%'
            },
            overlayCSS: {backgroundColor: '#FFF'}
        });
        
        $this.addClass('reloading');

        setTimeout(function () {
            $this.unblock();
            $this.removeClass('reloading');
        }, 900);

    }).on('click', '.panel > .panel-heading > .panel-tool-options li > a[data-rel="close"]', function (ev) {
        ev.preventDefault();

        var $this = $(this);
        var $panel = $this.closest('.panel');

        $panel.fadeOut(500, function () {
            $panel.remove();
        });

    }).on('click', '.panel > .panel-heading > .panel-tool-options li > a[data-rel="collapse"]', function (ev) {
        ev.preventDefault();

        var $this = $(this),
            $panel = $this.closest('.panel'),
            $body = $panel.children('.panel-body, .table'),
            do_collapse = !$panel.hasClass('panel-collapse');

        if ($panel.is('[data-collapsed="1"]')) {
            $panel.attr('data-collapsed', 0);
            $body.hide();
            do_collapse = false;
        }

        if (do_collapse) {
            $body.slideUp('normal');
            $panel.addClass('panel-collapse');
        }
        else {
            $body.slideDown('normal');
            $panel.removeClass('panel-collapse');
        }
    });

    // removeable-list -- remove parent elements
    var $removalList = $(".removeable-list");
    $(".removeable-list .remove").each(function () {
        var $this = $(this);
        $this.click(function (event) {
            event.preventDefault();

            var $parent = $this.parent('li');
            $parent.slideUp(500, function () {
                $parent.delay(3000).remove();

                if ($removalList.find("li").length == 0) {
                    $removalList.html('<li class="text-danger"><p>All items has been deleted.</p></li>');
                }
            });
        });
    });
})(jQuery);

/*
 * This function will remove its parent element
 *
 * @param $eleObj
 * @param $parentEle
 */

function removeElement($ele, $parentEle) {
    var $this = $($ele);
    $this.parent($parentEle).css({
        opacity: '0'
    });
}
