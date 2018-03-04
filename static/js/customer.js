$(window).on("load", function(){
  $.ajax({
      url: '/customer_list',
      data:'',
      type: 'POST',
      success: function(response) {
          $.each(response.message, function(index, customer){
          $("#customer_list").append('<option value="' + customer[2] + '">\
          '+customer[0]+' '+customer[1]+': '+customer[2]+'</option>');
        });
      },
      error: function(error) {
          console.log(error)
      }
  });
});

$(document).ready(function() {
    $('#TRN').blur(function() {
        $.ajax({
            url: '/select_customer',
            data:$('#TRN').serialize(),
            type: 'POST',
            success: function(response) {
              if (Object.keys(response).length > 1){
                $('#FirstName').val(response.FirstName);
                $('#LastName').val(response.LastName);
                $('#Company').val(response.Company);
                $('#Address').val(response.Address);
                $('#City').val(response.City);
                $('#Country').val(response.Country);
                $('#PostalCode').val(response.PostalCode);
                $('#Phone').val(response.Phone);
                $('#Email').val(response.Email);
                $('#Fax').val(response.Fax);
                $('#TRN').val(response.TRN);
                $('#TaxOffice').val(response.TaxOffice);
              }
            },
            error: function(error) {
                console.log(error)
            }
        });
    });
});
