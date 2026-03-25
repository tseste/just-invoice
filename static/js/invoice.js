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
          $("#product_list").append('<option value="' + product + '">' + product + '</option>');
        });
      },
      error: function(error) {
          console.log(error)
      }
  });
});
$(document).ready(function(){
  var invoiceI18n = window.invoiceI18n || {
    viewPdf: 'View PDF',
    searchPlaceholder: 'Search'
  };

  function parseNumber(value) {
    if (value === null || value === undefined) {
      return 0;
    }
    var normalized = String(value).replace(',', '.').trim();
    var parsed = parseFloat(normalized);
    return Number.isNaN(parsed) ? 0 : parsed;
  }

  function formatMoney(value) {
    return value.toFixed(2);
  }

  function recalculateInvoiceTotals() {
    var subtotal = parseNumber($('#Subtotal').val());
    var discountPercent = parseNumber($('#Discount').val());
    var vatPercent = parseNumber($('#VAT').val());

    // Clamp percentages to a safe range.
    if (discountPercent < 0) {
      discountPercent = 0;
    }
    if (discountPercent > 100) {
      discountPercent = 100;
    }
    if (vatPercent < 0) {
      vatPercent = 0;
    }

    var afterDiscount = subtotal * (1 - (discountPercent / 100));
    var vatPrice = afterDiscount * (vatPercent / 100);
    var totalDue = afterDiscount + vatPrice;

    $('#AfterDiscount').val(formatMoney(afterDiscount));
    $('#VATPrice').val(formatMoney(vatPrice));
    $('#TotalDue').val(formatMoney(totalDue));
    $('#Total').val(formatMoney(totalDue));
  }

  function updateSubtotal() {
    var subtotal = 0;
    $('#rowController').children('tr').each(function() {
      var rowPrice = parseNumber($(this).find("p[id^='Price']").text());
      subtotal += rowPrice;
    });
    $('#Subtotal').val(formatMoney(subtotal));
    recalculateInvoiceTotals();
  }

  function updateRowPrice(rowNum) {
    var quantity = parseNumber($('#Quantity' + rowNum).val());
    var unitPrice = parseNumber($('#UnitPrice' + rowNum).text());
    if (quantity > 0 && unitPrice > 0) {
      $('#Price' + rowNum).html(formatMoney(quantity * unitPrice));
    } else {
      $('#Price' + rowNum).html('');
    }
    updateSubtotal();
  }

  $('#print').prop('disabled', true);
  $('#Discount, #VAT').on('input change blur', recalculateInvoiceTotals);
  recalculateInvoiceTotals();
  $('#save').click(function() {
    $.each($('#rowController').children('tr'), function(){console.log(this.id)});
   $('#print').prop('disabled', false);
 });
 $('#print').click(function() {
   var items = [];
   $('#rowController').children('tr').each(function() {
     var rowNum = this.id.replace('row', '');
     var item = {
       ProductId: $('#ProductId' + rowNum).val() || '',
       Name: $('#Name' + rowNum).text() || '',
       UnitType: $('#UnitTypeId' + rowNum).text() || '',
       Quantity: $('#Quantity' + rowNum).val() || '',
       UnitPrice: $('#UnitPrice' + rowNum).text() || '',
       Price: $('#Price' + rowNum).text() || '',
     };
     if (item.ProductId || item.Name || item.Quantity || item.Price) {
       items.push(item);
     }
   });

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
         'Subtotal': document.getElementById('Subtotal').value,
         'Discount': document.getElementById('Discount').value,
         'AfterDiscount': document.getElementById('AfterDiscount').value,
         'VAT': document.getElementById('VAT').value,
         'VATPrice': document.getElementById('VATPrice').value,
         'TotalDue': document.getElementById('TotalDue').value,
         'Total': document.getElementById('Total').value,
         'Items': items,
       }),
       contentType: 'application/json;charset=UTF-8',
       type: 'POST',
       success: function(response) {
         $("#print").unbind();
         $('#print').wrap("<a href='/invoice/"+document.getElementById('InvoiceId').value+".pdf'</a>")
         $('#print').html(invoiceI18n.viewPdf);
         }
       ,
       error: function(error) {
           console.log(error)
       }
   });
 });

  function loadCustomerByTrn() {
    if (!$('#TRN').val()) {
      return;
    }
    $.ajax({
        url: '/select_customer',
        data: $('#TRN').serialize(),
        type: 'POST',
        success: function(response) {
          if (Object.keys(response).length > 1){
            const fullName = response.Full_Name ||
              [response.FirstName, response.LastName].filter(Boolean).join(' ');
            $('#Full_Name').val(fullName);
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

  $('#TRN').on('change blur', loadCustomerByTrn);

    var i=0;
    $("#add_row").click(
        function()
        {
          $('#rowController').append('<tr id="row'+(i)+'"></tr>');
            $('#row'+i).html(
          "<td scope='row'>\
          <input class='input-lg' type='text' name='ProductId' id='ProductId"+i+"' placeholder='"+invoiceI18n.searchPlaceholder+"' list='product_list' />\
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
              var currentRow = i;
              $('#ProductId'+currentRow).on('change blur', function() { fillRow(this); });
              $('#Quantity'+currentRow).on('input change blur', function() { updateRowPrice(currentRow); });
          i++;
    });

    $("#delete_row").click(
        function()
        {
          if(i>0)
            {
            $("#row"+(--i)).remove();
            updateSubtotal();
        }
      });
      fillRow = function(element) {
        if (!element.value) {
          return;
        }
        var row_num = element.id.replace('ProductId', '');
        $.ajax({
            url: '/select_product',
            data: JSON.stringify({'ProductId': element.value}),
            contentType: 'application/json;charset=UTF-8',
            type: 'POST',
            success: function(response) {
              if (Object.keys(response).length > 1){
                $('#Name'+row_num).html(response.Name);
                $('#UnitTypeId'+row_num).html(response.UnitTypeName || response.UnitTypeId);
                $('#UnitPrice'+row_num).html(response.UnitPrice);
                updateRowPrice(row_num);
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
