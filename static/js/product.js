$(window).on("load", function(){
  $.ajax({
      url: '/product_list',
      data:'',
      type: 'POST',
      success: function(response) {
          $.each(response.message, function(index, product){
          $("#product_list").append('<option value="' + product + '"></option>');
        });
      },
      error: function(error) {
          console.log(error)
      }
  });
});

$(document).ready(function() {
    $('#Name').blur(function() {
        $.ajax({
            url: '/select_product',
            data:$('#Name').serialize(),
            type: 'POST',
            success: function(response) {
              if (Object.keys(response).length > 1){
                $('#Name').val(response.Name);
                $('#Description').val(response.Description);
                $('#UnitTypeId option[value='+ response.UnitTypeId +']').prop('selected', true);
                $('#UnitPrice').val(response.UnitPrice);
              }
            },
            error: function(error) {
                console.log(error)
            }
        });
    });
});
