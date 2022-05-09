
function resetHomeUploadForm () {
    $(".image-section, .details-section").show();
    $("#nextButton").attr("data-action", "next");
    $("#nextButton").text("next");
}

function reportValidity(field) {
    let valid = field.validity.valid;
    if (!valid) {
        field.reportValidity();
        return false;
    }
    return true;
}

$(() => {
    const MAX_NUMBER_OF_IMAGES = 6;
    const MIN_NUMBER_OF_IMAGES = 4;
    let image_count = 0;
    $(() => {
        const url_parameters = location.search ? location.search.toLowerCase() : '';
        if (url_parameters.indexOf('upload_home=true') !== -1) {
            $('#uploadHome').click();
        }
    });

    $(() => {
        const addHomeForm = $('form');
        const show_form = addHomeForm.attr('data-show') ? addHomeForm.attr('data-show').toLowerCase() : '';
        if (show_form === 'true') {
            $('#uploadHome').click();
        }
    });


    $(".upload-form").hide();   // Hide the upload form on page load
    
    $("#uploadHome").on("click", (ev) => {
        $(".upload-form, .page-content, footer, .upload-form .details-section").toggle();
    });

    $("#cancelButton").on("click", (ev) => {
        $(".upload-form, .page-content, footer").toggle();
        // To reset form
        resetHomeUploadForm();
    });

    $(() => {   // Sets the default value for apartment_type select field if data-selected-value attribute is set
        let selectField = $(".custom-select.form-field");
        let preSelectedValue = selectField.attr("data-selected-value");
        if (preSelectedValue) {
            let selectOptions = selectField.children();
            $.each(selectOptions, function (index, value) { 
                let option = $(value); 
                if (option.attr('value') === preSelectedValue) {
                    option.attr('selected', true);
                    return false;
                }
            });
        }
    });

    $("#nextButton").on("click", (ev) => {
        const action = $(ev.target).attr("data-action");
        if (action === "next") {
            let first_section_valid = image_count >= MIN_NUMBER_OF_IMAGES;
            // let first_section_valid = true;
            if (first_section_valid) {
                $(".image-section, .details-section").toggle();
                $(ev.target).attr("data-action", "submit");
                $(ev.target).text("submit");
            } else {
                alert("Home images must be at least 4");
            }
        }else if (action === "submit") {
            let second_section_valid = true
            const inputFields = $(".details-section").find(".form-field");
            $.each(inputFields, (index, field) => {
                second_section_valid = reportValidity(field);
                return second_section_valid;
            });
            if (second_section_valid) {
                $("form").submit();
            }
            
        } 
    });

    $(".add-image-btn").on("click", (ev) => {
        ev.preventDefault();
        if (image_count <= MAX_NUMBER_OF_IMAGES) {
            let image_div = $(".image-section");
            let image_field_name = `image_${image_count}`;
            image_div.append(`<input type="file" class="form-control form-field" style="display:none;" name="${image_field_name}" accept="image/jpeg">`);
            let form_field = image_div.children().last();
            form_field.click();
            form_field.on("change", (ev) => {
                console.log(ev.target.files);
                const image_name = ev.target.files[0].name;
                image_div.append(`<span class="text-primary m-2">${image_name}</span>`);
                image_count++;
            });
        } else {
            alert("Maximum number of images reached");
        }
    });

});