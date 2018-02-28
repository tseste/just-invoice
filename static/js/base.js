$( window ).on( "load", function(){
        if (window.location.pathname == "/") {
            $("#home_url").addClass('active');
        }
        else if (window.location.pathname == "/invoice") {
            $("#invoice_url").addClass('active');
        }
        else if (window.location.pathname == "/customers") {
            $("#customers_url").addClass('active');
        }
});
