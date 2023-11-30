// /* Javascript for MyXBlock. */
// function MyXBlock(runtime, element) {
//     console.log("................................................................console log")

//     function updateCount(result) {
//         $('.count', element).text(result.count);
//     }

//     var handlerUrl = runtime.handlerUrl(element, 'increment_count');

//     $('p', element).click(function(eventObject) {
//         $.ajax({
//             type: "POST",
//             url: handlerUrl,
//             data: JSON.stringify({"hello": "world"}),
//             success: updateCount
//         });
//     });

//     $(function ($) {
//         /* Here's where you'd do things on page load. */
//     });
// }


function MyXBlock(runtime, element) {
    console.log("................................................................console log")

    $(element).find('.save-button').on('click', function () {
        console.log("................................................................console log")
        var formData = new FormData();
        var jupyterliteUrl = $(element).find('input[name=jupyterlite_url]').val();
        var default_notebook = $(element).find('#default_notebook').prop('files')[0];
        formData.append('jupyterlite_url', jupyterliteUrl);
        formData.append('default_notebook', default_notebook);

        runtime.notify('save', {
            state: 'start'
        });
        // Make an AJAX request to the handlerUrl
        $(this).addClass("disabled");
        $.ajax({
            url: runtime.handlerUrl(element, 'studio_submit'),
            dataType: 'json',
            cache: false,
            processData: false,      
            contentType: false,
            data: formData,
            type: 'POST',
            complete: function () {
                $(this).removeClass("disabled");
            },
            success: function (response) {
                if (response.errors.length > 0) {
                    response.errors.forEach(function (error) {
                        runtime.notify('error', {
                            "message": error,
                            "title": 'Form submission error'
                        });
                    });
                } else {
                    runtime.notify('save', { state: 'end' });
                }
            },
        });
    });

    $(element).find('.cancel-button').on('click', function () {
        console.log("................................................................console log")
        runtime.notify('cancel', {});
    });
}

