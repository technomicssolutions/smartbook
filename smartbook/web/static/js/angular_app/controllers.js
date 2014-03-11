function HomeController($scope, $element, $http, $timeout, share, $location)
{
  
}

function ExpenseController($scope, $element, $http, $timeout, $location) {

	$scope.expense_heads = [];
	$scope.expense_head = '';
    $scope.payment_mode = 'true';
    $scope.payment_mode_selection = true;

	$scope.init = function(csrf_token)
    {
        $scope.csrf_token = csrf_token;
        $scope.get_expense_head_list();
    }
    $scope.get_expense_head_list = function() {
    	$http.get('/expenses/expense_head_list/').success(function(data)
        {
        	$scope.expense_heads = data.expense_heads;
            $scope.expense_head = 'select';
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    $scope.payment_mode_change = function(payment_mode) {
        if(payment_mode == 'cheque') {
            $scope.payment_mode_selection = false;
            
            new Picker.Date($$('#check_date'), {
                // timePicker: true,
                positionOffset: {x: 5, y: 0},
                pickerClass: 'datepicker_bootstrap',
                useFadeInOut: !Browser.ie,
                format:'%d/%m/%Y',
                // minDate: 
                // onSelect: function(date){
                //     myHiddenField.set('value', date.format('%s');
                // } 
            
            });
        } else {
            $scope.payment_mode_selection = true;
        }
    }
}

function AddEditUserController($scope, $element, $http, $timeout, $location) {
    $scope.init = function(csrf_token, user_type)
    {
        $scope.popup = '';
        $scope.new_designation = '';
        $scope.csrf_token = csrf_token;
        $scope.user_type = user_type;
        // $scope.new_desiganation_flag = true;
        $scope.error_flag = true;
        $scope.designation_flag = false;
        $scope.message = '';
        $scope.designation = '';
        if ($scope.user_type == 'staff'){
            $scope.get_designation_list();
            $scope.designation = 'select';
        }
        
    }
    $scope.get_designation_list = function() {
         $http.get('/designation_list/').success(function(data)
        {
            $scope.designations = data.designations;
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    $scope.add_designation = function() {
        if($scope.designation == 'other') {
            $scope.popup = new DialogueModelWindow({
                'dialogue_popup_width': '384px',
                'message_padding': '0px',
                'left': '28%',
                'top': '175px',
                'height': '115px',
                'content_div': '#add_designation'
            });
            var height = $(document).height();
            $scope.popup.set_overlay_height(height);
            $scope.popup.show_content();
            // $scope.new_desiganation_flag = false;
        }
    }
    $scope.add_new_designation = function() {
        params = { 
            'new_designation':$scope.new_designation,
            "csrfmiddlewaretoken" : $scope.csrf_token
        }
        $http({
            method : 'post',
            url : "/add_designation/",
            data : $.param(params),
            headers : {
                'Content-Type' : 'application/x-www-form-urlencoded'
            }
        }).success(function(data, status) {
            
            if (data.result == 'error'){
                $scope.error_flag=true;
                $scope.message = data.message;
            } else {
                $scope.popup.hide_popup();
                $scope.get_designation_list();
                $scope.designation = $scope.new_designation;
                // $scope.new_desiganation_flag = true;
            }
        }).error(function(data, success){
            
        });
    }
    $scope.show_designation_list = function() {
        $scope.designation_flag = true;
        $('#designation_val').hide();
        $scope.designation = $('#designation_val').val();
    }
    $scope.selected_head = function(head_name) {
    	$scope.expense_head = head_name;
    }
    $scope.close_popup = function(){
        // $scope.new_desiganation_flag = true;
        $scope.popup.hide_popup();
    }
	
}

function PurchaseController($scope, $element, $http, $timeout, share, $location) {

    $scope.items = [];
    $scope.selected_item = '';
    $scope.vendor_name = '';
    $scope.brand_name = '';
    $scope.company_name = '';
    $scope.selecting_item = false;
    $scope.item_selected = false;
    $scope.purchase = {
        'purchase_items': [],
        'purchase_invoice_number': '',
        'vendor_invoice_number': '',
        'vendor_do_number': '',
        'vendor_invoice_date': '',
        'purchase_invoice_date': '',
        'brand': '',
        'vendor': '',
        'transport': '',
        'discount': '',
        'net_total': '',
        'purchase_expense': '',
        'grant_total': '',
        'vendor_amount': '',
    }
    $scope.purchase.vendor = 'select';
    $scope.purchase.brand = 'select';
    $scope.purchase.transport = 'select';
    $scope.init = function(csrf_token, invoice_number)
    {
        $scope.csrf_token = csrf_token;
        $scope.purchase.purchase_invoice_number = invoice_number;
        $scope.popup = '';

        new Picker.Date($$('#vendor_invoice_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
        new Picker.Date($$('#purchase_invoice_id'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });

        $scope.get_vendors();
        $scope.get_brands();
        $scope.get_companies();

        console.log("$scope.purchase.purchase_invoice_number ", $scope.purchase.purchase_invoice_number );
    }

    $scope.get_vendors = function() {
        $http.get('/vendor/list/').success(function(data)
        {
            $scope.vendors = data.vendors;
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    $scope.add_vendor = function() {
        if($scope.purchase.vendor == 'other') {
            $scope.popup = new DialogueModelWindow({
                'dialogue_popup_width': '384px',
                'message_padding': '0px',
                'left': '28%',
                'top': '40px',
                'height': '702px',
                'content_div': '#add_vendor'
            });
            var height = $(document).height();
            $scope.popup.set_overlay_height(height);
            $scope.popup.show_content();
        }
    }

    $scope.add_new_vendor = function() {
        params = { 
            'name':$scope.vendor_name,
            'contact_person': $scope.contact_person,
            'house': $scope.house_name,
            'street': $scope.street,
            'city': $scope.city,
            'district':$scope.district,
            'pin': $scope.pin,
            'mobile': $scope.mobile,
            'phone': $scope.land_line,
            'email': $scope.email_id,
            "csrfmiddlewaretoken" : $scope.csrf_token
        }
        $http({
            method : 'post',
            url : "/register/vendor/",
            data : $.param(params),
            headers : {
                'Content-Type' : 'application/x-www-form-urlencoded'
            }
        }).success(function(data, status) {
            
            if (data.result == 'error'){
                $scope.error_flag=true;
                $scope.message = data.message;
            } else {
                $scope.popup.hide_popup();
                $scope.get_vendors();
                $scope.purchase.vendor = $scope.vendor_name;
                $scope.purchase.vendor = data.vendor_name;
            }
        }).error(function(data, success){
            
        });
    }

    $scope.get_brands = function() {
        $http.get('/inventory/brand_list/').success(function(data)
        {
            $scope.brands = data.brands;
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    $scope.add_brand = function() {
        if($scope.purchase.brand == 'other') {
            $scope.popup = new DialogueModelWindow({
                'dialogue_popup_width': '384px',
                'message_padding': '0px',
                'left': '28%',
                'top': '150px',
                'height': '115px',
                'content_div': '#add_brand'
            });
            var height = $(document).height();
            $scope.popup.set_overlay_height(height);
            $scope.popup.show_content();
        }
    }

    $scope.add_new_brand = function() {
        params = { 
            'brand_name':$scope.brand_name,
            "csrfmiddlewaretoken" : $scope.csrf_token
        }
        $http({
            method : 'post',
            url : "/inventory/add/brand/",
            data : $.param(params),
            headers : {
                'Content-Type' : 'application/x-www-form-urlencoded'
            }
        }).success(function(data, status) {
            
            if (data.result == 'error'){
                $scope.error_flag=true;
                $scope.message = data.message;
            } else {
                $scope.popup.hide_popup();
                $scope.get_brands();
                $scope.purchase.brand = $scope.brand_name;
                
            }
        }).error(function(data, success){
            
        });
    }

    $scope.get_companies = function() {
        $http.get('/company_list/').success(function(data)
        {
            $scope.companies = data.company_names;
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    $scope.add_transport = function() {
        if($scope.purchase.transport == 'other') {
            $scope.popup = new DialogueModelWindow({
                'dialogue_popup_width': '384px',
                'message_padding': '0px',
                'left': '28%',
                'top': '150px',
                'height': '115px',
                'content_div': '#add_company'
            });
            var height = $(document).height();
            $scope.popup.set_overlay_height(height);
            $scope.popup.show_content();
        }
    }

    $scope.add_new_company = function() {
        params = { 
            'new_company':$scope.company_name,
            "csrfmiddlewaretoken" : $scope.csrf_token
        }
        $http({
            method : 'post',
            url : "/add_company/",
            data : $.param(params),
            headers : {
                'Content-Type' : 'application/x-www-form-urlencoded'
            }
        }).success(function(data, status) {
            
            if (data.result == 'error'){
                $scope.error_flag=true;
                $scope.message = data.message;
            } else {
                $scope.popup.hide_popup();
                $scope.get_companies();
                $scope.purchase.transport = $scope.company_name;
                
            }
        }).error(function(data, success){
            
        });
    }

    $scope.getItems = function(parameter){

        console.log('parameter', parameter);
        if(parameter == 'item_code')
            var param = $scope.item_code;
        else if(parameter == 'item_name')
            var param = $scope.item_name;
        else if (parameter == 'barcode')
            var param = $scope.barcode;
        $http.get('/inventory/items/?'+parameter+'='+param).success(function(data)
        {
            $scope.selecting_item = true;
            $scope.item_selected = false;
            $scope.items = data.items;
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }

    $scope.addPurchaseItem = function(item) {
        $scope.selecting_item = false;
        $scope.item_selected = true;
        $scope.item_code = '';
        $scope.item_name = '';
        $scope.barcode = '';
        var selected_item = {
            'item_code': item.item_code,
            'item_name': item.item_name,
            'barcode': item.barcode,
            'uom': item.uom,
            'current_stock': item.current_stock,
            'frieght': '',
            'frieght_unit': 0,
            'handling': '',
            'handling_unit': 0,
            'tax': item.tax,
            'selling_price': '',
            'qty_purchased': 0,
            'cost_price': '',
            'permit_disc_amt': '',
            'permit_disc_percent': '',
            'net_amount': '',
            'unit_price': 0,
            'expense': '',
            'expense_unit': 0
        }
        $scope.purchase.purchase_items.push(selected_item);
    }
    $scope.calculate_frieght = function(item){
        if(item.qty_purchased != '' && item.frieght != ''){
            item.frieght_unit = parseFloat(item.frieght)/parseFloat(item.qty_purchased);
        }
        $scope.calculate_net_amount(item);
        $scope.calculate_cost_price(item);
    }
    $scope.calculate_handling = function(item){
        if(item.qty_purchased != '' && item.handling != ''){
            item.handling_unit = parseFloat(item.handling)/parseFloat(item.qty_purchased);
        }
        $scope.calculate_cost_price(item);
        $scope.calculate_net_amount(item);
    }
    $scope.calculate_expense = function(item){
        if(item.qty_purchased != '' && item.expense != ''){
            item.expense_unit = parseFloat(item.expense)/parseFloat(item.qty_purchased);
        }
        $scope.calculate_cost_price(item);
        $scope.calculate_net_amount(item);
        $scope.calculate_purchase_expense();
    }
    $scope.calculate_cost_price = function(item) {
        if(item.unit_price != '' || item.frieght_unit != '' || item.handling_unit != '' || item.expense_unit != ''){
            item.cost_price = parseFloat(item.unit_price) + parseFloat(item.frieght_unit) + parseFloat(item.handling_unit) + parseFloat(item.expense_unit)
        }
        $scope.calculate_net_amount(item);
    }

    $scope.calculate_net_amount = function(item) {
        if(item.qty_purchased != '' && item.unit_price != ''){
            item.net_amount = ((parseFloat(item.qty_purchased)*parseFloat(item.unit_price)) + parseFloat(item.frieght_unit)+ parseFloat(item.handling_unit)+parseFloat(item.expense_unit)).toFixed(3);
        }
        $scope.calculate_vendor_amount();
        $scope.calculate_net_total();
    }
    $scope.calculate_discount_amt = function(item) {
        if((item.permit_disc_percent != '' || item.permit_disc_percent != 0) && (item.selling_price != '' || item.selling_price != 0)) {
            item.permit_disc_amt = (parseFloat(item.selling_price)*parseFloat(item.permit_disc_percent))/100;
        }
    }

    $scope.calculate_discount_percent = function(item) {
        if((item.permit_disc_amt != '' || item.permit_disc_amt != '') && (item.selling_price != '' || item.selling_price != 0)) {
            item.permit_disc_percent = (parseFloat(item.permit_disc_amt)/parseFloat(item.selling_price))*100;
        }
    }

    $scope.calculate_vendor_amount = function() {
        var vendor_amount = 0;
        for(i=0; i<$scope.purchase.purchase_items.length; i++){
            vendor_amount = vendor_amount + (parseFloat($scope.purchase.purchase_items[i].unit_price)*parseFloat($scope.purchase.purchase_items[i].qty_purchased));
        }

        $scope.purchase.vendor_amount = vendor_amount;
    }

    $scope.calculate_net_total = function(){
        var net_total = 0;
        for(i=0; i<$scope.purchase.purchase_items.length; i++){
            net_total = net_total + parseFloat($scope.purchase.purchase_items[i].net_amount);
        }
        $scope.purchase.net_total = net_total;
        $scope.calculate_grant_total();
    }

    $scope.calculate_purchase_expense = function(){
        var purchase_expense = 0;
        console.log('expense');
        for(i=0; i<$scope.purchase.purchase_items.length; i++){
            purchase_expense = purchase_expense + parseFloat($scope.purchase.purchase_items[i].expense);
        }
        $scope.purchase.purchase_expense = purchase_expense;
    }

    $scope.calculate_grant_total = function(){
        $scope.purchase.grant_total = $scope.purchase.net_total - $scope.purchase.discount;
    }
    $scope.validate_purchase = function() {
        if($scope.purchase.vendor_invoice_number == '') {
            $scope.validation_error = "Please Enter Vendor invoice number" ;
            return false;
        } else if($scope.purchase.vendor_do_number == ''){
            $scope.validation_error = "Please enter Vendor D.O number";
            return false;
        } else if($scope.purchase.vendor_invoice_date == '') {
            $scope.validation_error = "Please enter vendor invoice date";
            return false;
        } else if($scope.purchase.purchase_invoice_date == ''){
            $scope.validation_error = "Please enter purchase invoice date";
            return false;
        } else if($scope.purchase.beand == '') {
            $scope.validation_error = "Please select brand";
            return false;
        } else if($scope.purchase.vendor == '') {
            $scope.validation_error == "Please select vendor";
            return false;
        } else if($scope.purchase.trasport == '') {
            $scope.validation_error == "Please select Transportation company"
            return false;
        } else if($scope.purchase.purchase_items.length == 0){
            $scope.validation_error = "Please Choose Item";
            return false;
        } 
        else {
            return true;
        }        
    }

    $scope.save_purchase = function() {
        if($scope.validate_purchase) {
            params = { 
                'purchase': angular.toJson($scope.purchase),
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            $http({
                method : 'post',
                url : "/purchase/purchase-entry/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                
               
            }).error(function(data, success){
                
            });
        }
    }
}

function SalesController($scope, $element, $http, $timeout, share, $location) {

    $scope.items = [];
    $scope.selected_item = '';
    $scope.selecting_item = false;
    $scope.item_selected = false;
    $scope.sales_items = [];
    $scope.init = function(csrf_token)
    {
        $scope.csrf_token = csrf_token;
    }

    $scope.getItems = function(parameter){

        console.log('parameter', parameter);
        if(parameter == 'item_code')
            var param = $scope.item_code;
        else if(parameter == 'item_name')
            var param = $scope.item_name;
        else if (parameter == 'barcode')
            var param = $scope.barcode;
        $http.get('/inventory/items/?'+parameter+'='+param).success(function(data)
        {
            $scope.selecting_item = true;
            $scope.item_selected = false;
            $scope.items = data.items;
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }

    $scope.addSalesItem = function(item) {
        $scope.selecting_item = false;
        $scope.item_selected = true;
        $scope.item_code = '';
        $scope.item_name = '';
        $scope.barcode = '';
        var selected_item = {

            'item_code': item.item_code,
            'item_name': item.item_name,
            'barcode': item.barcode,
            'current_stock': item.current_stock,
            'unit_price': item.selling_price,
            'tax': item.tax,
            'tax_amount':0,
            'qty_sold': 0,
            'uom': item.uom,
            'discount_permit': item.discount_permit,
            'discount_permit_amount':0,
            'disc_given': 0,
            'unit_cost':0,
            'net_amount': 0,

            
        }
        $scope.calculate_tax_amount_sale(selected_item);
        $scope.calculate_discount_amount_sale(selected_item);
        $scope.calculate_unit_cost_sale(selected_item);
        $scope.sales_items.push(selected_item);
    }
    
    
    $scope.calculate_net_amount_sale = function(item) {
        if(item.qty_sold != '' && item.unit_price != ''){
            item.net_amount = ((parseFloat(item.qty_sold)*parseFloat(item.unit_price))+parseFloat(item.tax_amount)-parseFloat(item.disc_given)).toFixed(2);
            
        }
    }
    $scope.calculate_tax_amount_sale = function(item) {
        if(item.tax != '' && item.unit_price != ''){
            item.tax_amount = (parseFloat(item.unit_price)*parseFloat(item.tax))/100;
        }
    }
    $scope.calculate_discount_amount_sale = function(item) {
        if(item.discount_permit != '' && item.unit_price != ''){
            item.discount_permit_amount = (parseFloat(item.unit_price)*parseFloat(item.discount_permit))/100;
        }
    }
    $scope.calculate_unit_cost_sale = function(item) {
        if(item.unit_price != ''){
            item.unit_cost = (parseFloat(item.unit_price)+parseFloat(item.tax_amount)-parseFloat(item.disc_given)).toFixed(2);
            
        }
    }
}