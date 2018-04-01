$(window).on("load", function(){
  $.ajax({
      url: '/customer_list',
      data:'',
      type: 'POST',
      success: function(response) {
          $.each(response.message, function(index, customer){
          $("#billingTRNlist").append('<option value="' + customer[1] + '">\
          '+customer[0]+': '+customer[1]+'</option>');
        });
      },
      error: function(error) {
          console.log(error)
      }
  });
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
$(document).ready(function(){
  $('#print').prop('disabled', true);
  $('#save').click(function() {
    $.each($('#rowController').children('tr'), function(){console.log(this.id)});
   $('#print').prop('disabled', false);
 });
 $('#print').click(function() {
   $('#print').html('<i class="fas fa-spinner fa-spin"></i>');
   $.ajax({
       url: 'invoice/create_pdf',
       data: JSON.stringify({
         'Full_Name': document.getElementById('Full_Name').value,
         'BillingAddress': document.getElementById('BillingAddress').value,
         'BillingCity': document.getElementById('BillingCity').value,
         'BillingCountry': document.getElementById('BillingCountry').value,
         'BillingPostalCode': document.getElementById('BillingPostalCode').value,
         'Company': document.getElementById('Company').value,
         'TRN': document.getElementById('TRN').value,
         'TaxOffice': document.getElementById('TaxOffice').value,
         'InvoiceId': document.getElementById('InvoiceId').value,
         'datepicker1': document.getElementById('datepicker1').value,
         'datepicker2': document.getElementById('datepicker2').value,
         'Total': document.getElementById('Total').value,
       }),
       contentType: 'application/json;charset=UTF-8',
       type: 'POST',
       success: function(response) {
         $("#print").unbind();
         $('#print').wrap("<a href='/invoice/"+document.getElementById('InvoiceId').value+".pdf'</a>")
         $('#print').html('Δείτε το pdf.');
         }
       ,
       error: function(error) {
           console.log(error)
       }
   });
 });

  $('#TRN').blur(function() {
    if ($('#TRN').val()){
      $.ajax({
          url: '/select_customer',
          data:$('#TRN').serialize(),
          type: 'POST',
          success: function(response) {
            if (Object.keys(response).length > 1){
              $('#Full_Name').val(response.Full_Name);
              $('#BillingAddress').val(response.Address);
              $('#BillingCity').val(response.City);
              $('#BillingCountry').val(response.Country);
              $('#BillingPostalCode').val(response.PostalCode);
              $('#Company').val(response.Company);
              $('#TaxOffice').val(response.TaxOffice);
            }
          },
          error: function(error) {
              console.log(error)
          }
      });
    }
  });

    var i=0;
    $("#add_row").click(
        function()
        {
          $('#rowController').append('<tr id="row'+(i)+'"></tr>');
            $('#row'+i).html(
          "<td scope='row'>\
          <input class='input-lg' type='text' onblur='fillRow(this)' name='ProductId' id='ProductId"+i+"' placeholder='Αναζήτηση' list='product_list' />\
          </td>\
          <td>\
          <p name='Name' id='Name"+i+"' ></p>\
          </td>\
          <td>\
          <p name='UnitTypeId' id='UnitTypeId"+i+"' ></p>\
          </td>\
          <td>\
          <input class='input-md' type='text' name='Quantity' id='Quantity"+i+"'/>\
          </td>\
          <td>\
          <p type='text' name='UnitPrice' id='UnitPrice"+i+"'></p>\
          </td>\
          <td>\
          <p name='Price' id='Price"+i+"'></p>\
          </td>");
          i++;
    });

    $("#delete_row").click(
        function()
        {
          if(i>0)
            {
            $("#row"+(--i)).remove();
        }
      });
      fillRow = function(element) {
        var row_num = element.id.slice(element.id.length-1);
        $.ajax({
            url: '/select_product',
            data: JSON.stringify({'ProductId': element.value}),
            contentType: 'application/json;charset=UTF-8',
            type: 'POST',
            success: function(response) {
              if (Object.keys(response).length > 1){
                $('#Name'+row_num).html(response.Name);
                $('#UnitPrice'+row_num).html(response.UnitPrice);
              }
            },
            error: function(error) {
                console.log(error)
            }
        });
      }
    $('#datepicker1').datepicker({dateFormat: 'dd/mm/yy'});
    $('#datepicker2').datepicker({dateFormat: 'dd/mm/yy'});
  });
