$(document).ready(function () {
    $('#id_phone').inputmask({
        "mask": "+\\9\\98(99) 999-99-99"
    });
});

$(document).ready(function () {
    var translations = $('#translation-data').data();  // Fetch the data attributes
    var selectText = translations.select;  // Get the translation for 'Select'

    $('#id_region').change(function () {  // Updated selector for region
        var regionId = $(this).val();
        if (regionId) {
            var url = $('#get-districts-url').val().replace('0', regionId);
            $.ajax({
                url: url,
                data: {'region_id': regionId},
                success: function (data) {
                    var districtSelect = $('#id_district');  // Updated selector for district
                    districtSelect.empty();
                    districtSelect.append('<option value="">' + selectText + '</option>');
                    $.each(data, function (index, district) {
                        districtSelect.append('<option value="' + district.id + '">' + district.name + '</option>');
                    });
                }
            });
        } else {
            $('#id_district').empty();
            $('#id_district').append('<option value="">' + selectText + '</option>');
        }
    });
});
