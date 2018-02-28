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
$(document).ready(function(){
  var step = 1;
  $(document).on("click",".next", function () {
    $(this).parents('section').fadeOut(500);
    $('#step-' + String(++step)).fadeIn(4000);


  });
  $(document).on("click",".previous", function () {
    $(this).parents('section').fadeOut(500);
    $('#step-' + String(--step)).fadeIn(4000);
  });
    var i=1;
    $("#add_row").click(
        function()
        {
            $('#addr'+i).html(
          "<td class='text-center'>"+
                (i+1)+
          "</td>\
          <td>\
          <input type='text' name='product_name"+i+"' id='product_name"+i+"' onblur='fillit(this.id)' class='form-control' >\
          </td>\
          <td>\
          <input type='text' name='product_mu"+i+"' id='product_mu"+i+"' class='form-control' >\
          </td>\
          <td>\
          <input type='text' name='quantity"+i+"' id='quantity"+i+"' onchange='calcit(this.id)' />\
          </td>\
          <td>\
          <input type='text' name='units0' id='units0' />\
          </td>\
          <td>\
          <input type='text' name='product_up"+i+"' id='product_up"+i+"' class='form-control' >\
          </td>\
          <td>\
          <input type='text' name='fpa"+i+"' id='fpa"+i+"'  class='form-control'/>\
          </td>\
          <td>\
          <input type='text' name='total"+i+"' id='total"+i+"' />\
          </td>\
            </tr>"
            );
    $('#tab_logic').append('<tr id="addr'+(i+1)+'"></tr>');
        i++;
    });

    $("#delete_row").click(
        function()
        {
          if(i>1)
            {
            $("#addr"+(i-1)).html('');
            i--;
        }
      }
    );
    $('#datepicker').datepicker({uiLibrary: 'bootstrap4'});
    $('#customer_name').blur(function() {
        $.ajax({
            url: '/select_user',
            data:$('#customer_name').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
                $('#customer_name').val(response.customer_name);
                $('#customer_job').val(response.customer_job);
                $('#customer_afm').val(response.customer_afm);
                $('#customer_doy').val(response.customer_doy);
                $('#customer_address').val(response.customer_address);
            },
            error: function(error) {
                console.log(error)
            }
        });
    });

    fillit = function (pid){
        var pidnum = pid.slice(-1)
        $.ajax({
            url: '/select_product',
            data:$('#product_name'+pidnum).serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
                $('#product_name'+pidnum).val(response.product_name);
                $('#product_mu'+pidnum).val(response.product_mu);
                $('#quantity'+pidnum).val(1);
                $('#product_up'+pidnum).val(response.product_up);
                $('#total'+pidnum).val(response.product_up);
            },
            error: function(error) {
                console.log(error)
            }
        });
    };

    calcit = function (qid)
    {
        var q = parseFloat($('#'+qid).val());
        var qidnum = qid.slice(-1)
        var t = q*parseFloat($('#product_up'+qidnum).val())
        $('#total'+qidnum).val(t);

    };

    totalit = function (tid)
    {
        var bt = 0
        for (j=0;j<i;j++)
        {
            bt += parseFloat($('#total'+j).val());
        }
        $('#'+tid).val(bt);
    };

    fpait = function (fid)
    {
        var st = parseFloat($('#total').val()) + parseFloat($('#total').val())*parseFloat($('#'+fid).val())/100
        $('#invoice_total').val(st.toFixed(2));
    };
});
