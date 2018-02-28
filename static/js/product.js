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

  $.ajax({
      url: '/product_types_list',
      data:'',
      type: 'POST',
      success: function(response) {
          $.each(response.message, function(index, ProductType){
          $("#UnitTypeId").append('<option value="' + ProductType[0] + '">'+ ProductType[1] +'</option>');
        });
      },
      error: function(error) {
          console.log(error)
      }
  });
});

$(document).ready(function() {
    $('#btnaddProduct').click(function() {

        $.ajax({
            url: '/add_product',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log('success');
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

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
