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

        // Show modal with animation
        setTimeout(function () {
            modal.addClass('show');
        }, 10);

        // Close modal on click outside modal content
        modal.click(function () {
            removeModal();
        });

        // Close modal on ESC key press
        $('body').on('keyup.modal-close', function (e) {
            if (e.key === 'Escape') {
                removeModal();
            }
        });

        // Toggle image size on click
        modalImg.click(function () {
            modalImg.toggleClass('enlarged');
        });
    });
});
