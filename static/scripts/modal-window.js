$(document).ready(function () {
    $('img[data-enlargeable]').addClass('img-enlargeable').click(function () {
        var src = $(this).attr('src');
        var modal, modalImg;

        function removeModal() {
            modal.removeClass('show');
            setTimeout(function () {
                modal.remove();
            }, 300);
            $('body').off('keyup.modal-close');
        }

        modalImg = $('<img>').attr('src', src).addClass('enlarged');

        modal = $('<div>').addClass('modal').append(
            $('<div>').addClass('modal-container').append(modalImg)
        ).appendTo('body');

        setTimeout(function () {
            modal.addClass('show');
        }, 10);

        modal.click(function () {
            removeModal();
        });

        $('body').on('keyup.modal-close', function (e) {
            if (e.key === 'Escape') {
                removeModal();
            }
        });

        modalImg.click(function () {
            modalImg.toggleClass('enlarged');
        });
    });
});
