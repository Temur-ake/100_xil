$(document).ready(function () {
    $('#id_phone').inputmask({
        "mask": "+\\9\\98(99) 999-99-99"
    });
});

$(document).ready(function () {
    var translations = $('#translation-data').data();  // Fetch the data attributes
    var selectText = translations.select;  // Get the translation for 'Select'

    $('#id_currier-0-region').change(function () {
        var regionId = $(this).val();
        if (regionId) {
            var url = $('#get-districts-url').val().replace('0', regionId);
            $.ajax({
                url: url,
                data: {'region_id': regionId},
                success: function (data) {
                    var districtSelect = $('#id_currier-0-district');
                    districtSelect.empty();
                    districtSelect.append('<option value="">' + selectText + '</option>');
                    $.each(data, function (index, district) {
                        districtSelect.append('<option value="' + district.id + '">' + district.name + '</option>');
                    });
                }
            });
        } else {
            $('#id_currier-0-district').empty();
            $('#id_currier-0-district').append('<option value="">' + selectText + '</option>');
        }
    });
});
