function HomeController($scope, $element, $http, $timeout, share, $location)
{
  
}

function ExpenseController($scope, $element, $http, $timeout, $location) {

	$scope.expense_heads = [];
	$scope.expense_head = '';
    $scope.payment_mode = 'cash';
    $scope.payment_mode_selection = true;
    $scope.voucher_no = '';
    $scope.is_valid = false;
    $scope.error_flag = false;
    $scope.error_message = '';

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
            
            new Picker.Date($$('#cheque_date'), {
                timePicker: false,
                positionOffset: {x: 5, y: 0},
                pickerClass: 'datepicker_bootstrap',
                useFadeInOut: !Browser.ie,
                format:'%d/%m/%Y',
            });
        } else {
            $scope.payment_mode_selection = true;
        }
    }
    $scope.reset = function() {
        $scope.expense_head = 'select';
        $scope.amount = '';
        $scope.payment_mode = 'cash';
        $scope.payment_mode_selection = true;
        $scope.narration = '';
        $scope.cheque_no = '';
        $scope.cheque_date = '';
        $scope.branch = '';
        $scope.bank_name = '';
        $scope.cheque_date = $$('#cheque_date').set('value', '');
    }
    $scope.form_validation = function(){
        $scope.voucher_no = $$('#voucher_no')[0].get('value');
        $scope.date = $$('#date')[0].get('value');
        $scope.cheque_date = $$('#cheque_date')[0].get('value');
        if ($scope.expense_head == '' || $scope.expense_head == undefined || $scope.expense_head == 'select') {
            $scope.error_flag = true;
            $scope.error_message = 'Please choose expense head';
            return false;
        } else if ($scope.amount == '' || $scope.amount == undefined) {
            $scope.error_flag = true;
            $scope.error_message = 'Please enter amount';
            return false;
        } else if ($scope.narration == '' || $scope.narration == undefined) {
            $scope.error_flag = true;
            $scope.error_message = 'Please add narration';
            return false;
        } else if( $scope.payment_mode == 'cheque' && ($scope.cheque_no == '' || $scope.cheque_no == undefined)) {
            $scope.error_flag = true;
            $scope.error_message = 'Please add cheque no';
            return false;
        } else if( $scope.payment_mode == 'cheque' && ($scope.cheque_date == '' || $scope.cheque_date == undefined)) {
            $scope.error_flag = true;
            $scope.error_message = 'Please add cheque date';
            return false;
        } else if( $scope.payment_mode == 'cheque' && ($scope.bank_name == '' || $scope.bank_name == undefined)) {
            $scope.error_flag = true;
            $scope.error_message = 'Please add bank name';
            return false;
        } else if( $scope.payment_mode == 'cheque' && ($scope.branch == '' || $scope.branch == undefined)) {
            $scope.error_flag = true;
            $scope.error_message = 'Please add branch';
            return false;
        }
        return true;
    }
    $scope.save_expense = function(){
        $scope.is_valid = $scope.form_validation();
        if ($scope.is_valid) {
            $scope.error_flag = false;
            $scope.error_message = '';
            params = { 
                'voucher_no':$scope.voucher_no,
                'date': $scope.date,
                'head_name': $scope.expense_head,
                'amount': $scope.amount,
                'payment_mode': $scope.payment_mode,
                'cheque_date':$scope.cheque_date,
                'cheque_no': $scope.cheque_no,
                'bank_name': $scope.bank_name,
                'branch': $scope.branch,
                'narration': $scope.narration,
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            $http({
                method : 'post',
                url : "/expenses/new_expense/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                
                if (data.result == 'error'){
                    $scope.error_flag=true;
                    $scope.message = data.message;
                } else {
                    $scope.error_flag=false;
                    $scope.message = '';
                    console.log('success');
                    document.location.href ='/';
                }
            }).error(function(data, status){
                console.log(data);
            });
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
                'dialogue_popup_width': '27%',
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
                $scope.error_flag=false;
                $scope.message = '';
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
        'deleted_items': []
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
        new Picker.Date($$('#purchase_invoice_date'), {
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
                'dialogue_popup_width': '36%',
                'message_padding': '0px',
                'left': '28%',
                'top': '40px',
                'height': 'auto',
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
                $scope.vendor_name = '';
                $scope.contact_person = '';
                $scope.house_name = '';
                $scope.street = '';
                $scope.city = '';
                $scope.district = '';
                $scope.pin = '';
                $scope.mobile = '';
                $scope.land_line = '';
                $scope.email_id = '';


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
                'dialogue_popup_width': '27%',
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
                $scope.error_flag=false;
                $scope.message = '';
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
                'dialogue_popup_width': '27%',
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
                $scope.company_name = '';
                $scope.error_flag=false;
                $scope.message = '';
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
        $scope.item_select_error = '';
        if($scope.purchase.purchase_items.length > 0) {
            for(var i=0; i< $scope.purchase.purchase_items.length; i++) {
                if($scope.purchase.purchase_items[i].item_code == item.item_code) {
                    $scope.item_select_error = "Item already selected";
                    return false;
                }
            }
        } 
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
    $scope.delete_purchase_item = function(item){
        var index = $scope.purchase.purchase_items.indexOf(item);
        $scope.purchase.purchase_items.splice(index, 1);
        $scope.purchase.deleted_items.push(item);
        console.log($scope.purchase.purchase_items, index);
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
        } else if($scope.purchase.brand == '') {
            $scope.validation_error = "Please select brand";
            return false;
        } else if($scope.purchase.vendor == '') {
            $scope.validation_error == "Please select vendor";
            return false;
        } else if($scope.purchase.trasport == '') {
            $scope.validation_error == "Please select Transportation company";
            return false;
        } else if($scope.purchase.purchase_items.length == 0){
            $scope.validation_error = "Please Choose Item";
            return false;
        } else if(typeOf($scope.purchase.vendor_invoice_number) != 'number') {
            $scop.validation_error = "Please enter a number as invoice number";
            return false;
        } else if(typeOf($scope.purchase.sales_invoice_number) != 'number') {
            $scop.validation_error = "Please enter a number as invoice number";
            return false;
        } else if(typeOf($scope.purchase.vendor_do_number) != 'number') {
            $scop.validation_error = "Please enter a number as vendor do number";
            return false;
        } else if(typeOf($scope.purchase.discount) != 'number') {
            $scop.validation_error = "Please enter a number as discount";
        }
        else {
            return true;
        }        
    }

    $scope.save_purchase = function() {
        if($scope.validate_purchase()) {
            $scope.purchase.purchase_invoice_date = $$('#purchase_invoice_date')[0].get('value');
            $scope.purchase.vendor_invoice_date = $$('#vendor_invoice_date')[0].get('value');
            params = { 
                'purchase': angular.toJson($scope.purchase),
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            $http({
                method : 'post',
                url : "/purchase/entry/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                document.location.href = '/purchase/entry/';
               
            }).error(function(data, success){
                
            });
        }
    }

    $scope.load_purchase = function() {
        $http.get('/purchase/?invoice_no='+$scope.purchase.purchase_invoice_number).success(function(data)
        {
            $scope.selecting_item = true;
            $scope.item_selected = false;
            $scope.purchase = data.purchase;
            $scope.purchase.deleted_items = [];
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }

    $scope.close_popup = function(){
        $scope.popup.hide_popup();
    }
}

function SalesController($scope, $element, $http, $timeout, share, $location) {

    $scope.items = [];
    $scope.selected_item = '';
    $scope.customer = '';
    $scope.staff = '';
    $scope.selecting_item = false;
    $scope.item_selected = false;
    $scope.payment_mode = 'cash';
    $scope.payment_mode_selection = true;
    $scope.sales = {
        'sales_items': [],
        'sales_invoice_number': '',
        'date_sales': '',
        'customer':'',
        'staff': '',
        'net_total': 0,
        'net_discount': 0,
        'roundoff': 0,
        'grant_total': 0,
        'paid': 0,
        'balance': 0,
        
    }
    $scope.sales.staff = 'select';
    $scope.sales.customer = 'select';
    $scope.init = function(csrf_token, sales_invoice_number)
    {
        $scope.csrf_token = csrf_token;
        $scope.sales.sales_invoice_number = sales_invoice_number;
        $scope.popup = '';
        
        
        $scope.get_staff();
        $scope.get_customers();
            
        console.log("$scope.sales.sales_invoice_number ", $scope.sales.sales_invoice_number );
    }
    $scope.payment_mode_change_sales = function(payment_mode) {
        if(payment_mode == 'cheque') {
            $scope.payment_mode_selection = false;
            
            var date_picker = new Picker.Date($$('#sales_invoice_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
            
        } else {
            $scope.payment_mode_selection = true;
        }
    }
    $scope.validate_sales = function() {
        if($scope.sales.sales_invoice_date == '') {
            $scope.validation_error = "Enter Sales invoice Date" ;
            return false;
        } else if($scope.sales.customer =='select'){
            $scope.validation_error = "Enter Customer Name";
            return false;
        } else if($scope.sales.staff =='select') {
            $scope.validation_error = "Enter Salesman Name";
            return false;
        } else if($scope.sales.sales_items.length == 0){
            $scope.validation_error = "Choose Item";
            return false;
        } 
        else {
            return true;
        }        
    }


    $scope.get_staff = function() {
        $http.get('/staff/list/').success(function(data)
        {
            $scope.staffs = data.staffs;

        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
        $scope.add_staff = function() {

        if($scope.sales.staff == 'other') {

            $scope.popup = new DialogueModelWindow({
                'dialogue_popup_width': '384px',
                'message_padding': '0px',
                'left': '28%',
                'top': '40px',
                'height': '702px',
                'content_div': '#'
            });
            var height = $(document).height();
            $scope.popup.set_overlay_height(height);
            $scope.popup.show_content();
        }
    }

    $scope.add_new_staff = function() {
        params = { 
            'name':$scope.staff_name,
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
            url : "/register/staff/",
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
                $scope.get_staff();
                $scope.sales.staff = $scope.staff_name;
                $scope.sales.staff = data.staff_name;
            }
        }).error(function(data, success){
            
        });
    }

    $scope.get_customers = function() {
        $http.get('/customer/list/').success(function(data)
        {   
            
            $scope.customers = data.customers;

        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
        $scope.add_customer = function() {

        if($scope.sales.customer == 'other') {


            $scope.popup = new DialogueModelWindow({
                'dialogue_popup_width': '36%',
                'message_padding': '0px',
                'left': '28%',
                'top': '40px',
                'height': 'auto',
                'content_div': '#add_customer'
            });
            var height = $(document).height();
            $scope.popup.set_overlay_height(height);
            $scope.popup.show_content();
        }
    }
    $scope.close_popup = function(){
        $scope.popup.hide_popup();
    }

    $scope.add_new_customer = function() { 
        params = { 
            'name':$scope.customer_name,
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
            url : "/register/customer/",
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
                $scope.get_customers();

                $scope.sales.customer = $scope.customer_name;
                $scope.sales.customer = data.customer_name;
            }
        }).error(function(data, success){
            
        });
    }

    $scope.items = [];
    $scope.selected_item = '';
    $scope.selecting_item = false;
    $scope.item_selected = false;
    $scope.sales_items = [];
    
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
       
        $scope.sales.sales_items.push(selected_item);
    }
    
    
    $scope.calculate_net_amount_sale = function(item) {
        if(item.qty_sold != '' && item.unit_price != ''){
            item.net_amount = ((parseFloat(item.qty_sold)*parseFloat(item.unit_price))+parseFloat(item.tax_amount)-parseFloat(item.disc_given)).toFixed(2);
            $scope.calculate_net_discount_sale();
        }
        $scope.calculate_net_total_sale();
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

    $scope.calculate_net_total_sale = function(){
        var net_total = 0;
        for(i=0; i<$scope.sales.sales_items.length; i++){
            net_total = net_total + parseFloat($scope.sales.sales_items[i].net_amount);
        }
        $scope.sales.net_total = net_total;
        $scope.calculate_grant_total_sale();
        
    }
    $scope.calculate_net_discount_sale = function(){
        
        var net_discount = 0;
        for(i=0; i<$scope.sales.sales_items.length; i++){
           
            net_discount = net_discount + parseFloat($scope.sales.sales_items[i].disc_given);

        }
        $scope.sales.net_discount = net_discount;
        
    }


    $scope.calculate_grant_total_sale = function(){
        $scope.sales.grant_total = $scope.sales.net_total   - $scope.sales.roundoff;
    }
    $scope.calculate_balance_sale = function () {
        $scope.sales.balance = $scope.sales.grant_total - $scope.sales.paid;
    }
    $scope.save_sales = function() {
        if($scope.validate_sales()) {

            $scope.sales.sales_invoice_date = $$('#sales_invoice_date')[0].get('value');
            
            params = { 
                'sales': angular.toJson($scope.sales),
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            $http({
                method : 'post',
                url : "/sales/entry/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                //document.location.href = '/sales/entry/';
               
            }).error(function(data, success){
                
            });
        }
    }

}

function DailyReportController($scope, $element, $http, $timeout, $location){    

    $scope.start_date = '';
    $scope.end_date = '';
    $scope.error_flag = false;

    $scope.init = function(){ 
        $scope.error_flag = false;      
        new Picker.Date($$('#start_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
        new Picker.Date($$('#end_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
    }
    $scope.view_report = function(report_type){
        $scope.error_flag = false;
        $scope.start_date = $$('#start_date')[0].get('value');
        $scope.end_date = $$('#end_date')[0].get('value');
        if ($scope.start_date == '' || $scope.start_date == undefined ){
            $scope.error_flag = true;
            $scope.messages = 'Please choose Start date';
        } else if($scope.end_date == '' || $scope.end_date == undefined ){
            $scope.error_flag = true;
            $scope.messages = 'Please choose End date';
        } else {
    
            $http.get('/reports/daily_report/?start_date='+$scope.start_date+'&end_date='+$scope.end_date).success(function(data){
                          
                $scope.daily_reports = data['daily_report'];
                $scope.daily_report_sales = data['daily_report_sales'][0];
                
            });
        }
    }

}

function VendorAccountController($scope, $element, $http, $timeout, $location){  
    $scope.actual_total_amount = 0;
    $scope.actual_amount_paid = 0;
    $scope.actual_balance_amount = 0; 
    $scope.cash = true; 
    $scope.init = function(csrf_token) 
    {
        $scope.csrf_token = csrf_token;
        $scope.vendor_account = {
            'payment_mode': 'cash',
            'total_amount': 0,
            'balance_amount': 0,
            'amount_paid': 0,
        }
        $scope.date_picker = new Picker.Date($$('#vendor_account_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format: '%d/%m/%Y',
        });
        $scope.date_picker_cheque = new Picker.Date($$('#cheque_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format: '%d/%m/%Y',
        });
    }
    $scope.select_payment_mode = function(){
        console.log('payment mode', $scope.vendor_account.payment_mode);
        if($scope.vendor_account.payment_mode == 'cheque') {
            $scope.cash = false;
        } else {
            $scope.cash = true;
        }
    }
    $scope.get_vendor_account_details = function(){
        var vendor = $scope.vendor_account.vendor;
        $http.get('/purchase/vendor_account/'+$scope.vendor_account.vendor+'/').success(function(data, status)
        {
            if (status==200) {             
                $scope.vendor_account = data.vendor_account;
                $scope.actual_total_amount = data.vendor_account.total_amount;
                $scope.actual_amount_paid = data.vendor_account.amount_paid;
                $scope.actual_balance_amount = data.vendor_account.balance_amount;
                $scope.select_payment_mode();               
            }
            
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    $scope.validate_vendor_account = function(){
        if($scope.vendor_account.vendor == '') {
            $scope.validation_error = "Please select Vendor";
            return false;
        } else if($scope.vendor_account.amount == ''){
            $scope.validation_error = "Please enter amount";            
            return false;
        } else if($$('#vendor_account_date')[0].get('value') == '') {
            $scope.validation_error = "Please select date";
            return false;
        }
        if(!$scope.vendor_account.narration){
            $scope.vendor_account.narration = "null";
        }
        if($scope.vendor_account.payment_mode == 'cash') {
            if(!$scope.vendor_account.branch_name)
                $scope.vendor_account.branch_name = "null";
            if(!$scope.vendor_account.bank_name)
                $scope.vendor_account.bank_name = "null";
            if(!$scope.vendor_account.cheque_no)
                $scope.vendor_account.cheque_no = "null";
            if(!$scope.vendor_account.cheque_date)
                $scope.vendor_account.cheque_date = "null";
        } else {
            if(!$scope.vendor_account.branch_name){
                $scope.validation_error = "Please enter branch name";
                return false;
            } else if(!$scope.vendor_account.bank_name){
                $scope.validation_error = "Please enter bank name";
                return false;
            }else if(!$scope.vendor_account.cheque_no){
                $scope.validation_error = "Please enter cheque no";
                return false;
            }else if($$('#cheque_date')[0].get('value') == ''){
                $scope.validation_error = "Please enter cheque date";
                return false;
            }
            if($$('#cheque_date')[0].get('value') != '') {
                $scope.vendor_account.cheque_date = $$('#cheque_date')[0].get('value');
            }
        }
        return true;
    }
    $scope.reset_vendor_account = function(){
        $scope.vendor_account.vendor = '';
        
    }
    $scope.calculate_vendor_account_amounts = function(){
        if($scope.actual_total_amount != 0 && $scope.actual_balance_amount != 0) {
            var total_amount = $scope.actual_total_amount;
            var balance_amount = $scope.actual_balance_amount;
            var amount_paid = $scope.actual_amount_paid;
            var amount = $scope.vendor_account.amount
            $scope.vendor_account.amount_paid = parseInt(amount) + parseInt(amount_paid);
            if(parseInt(balance_amount) > parseInt(amount) ) {
                $scope.vendor_account.balance_amount = parseInt(balance_amount) - parseInt(amount);
            } else {
                $scope.vendor_account.balance_amount = 0
            } 
        }
        
         
    }
    $scope.save_vendor_account = function(){
        $scope.vendor_account.vendor_account_date = $$('#vendor_account_date')[0].get('value');
        
        if($scope.validate_vendor_account()) {
            params = { 
                'vendor_account': angular.toJson($scope.vendor_account),
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            $http({
                method : 'post',
                url : '/purchase/vendor_account/'+$scope.vendor_account.vendor+'/',
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                document.location.href = '/purchase/vendor_accounts/';
               
            }).error(function(data, success){
                
            });
        }
        /*$scope.vendor_account.vendor_account_date = $$('#vendor_account_date')[0].get('value');
        $scope.vendor_account.total_amount = $scope.vendor_account.total_amount.toString();
        $scope.vendor_account.balance_amount = $scope.vendor_account.balance_amount.toString();
        $scope.vendor_account.amount_paid = $scope.vendor_account.amount_paid.toString();
*/       
    }
}

function PurchaseReportController($scope, $element, $http, $location) {
    $scope.report_name = 'date';
    $scope.start_date = '';
    $scope.end_date = '';
    $scope.report_type = '';
    $scope.vendor_name = 'select';
    $scope.purchase_amount_total = '';
    $scope.report_date_wise = true;
    $scope.report_vendor_wise = false;
    $scope.date_total_amount_flag = false;
    $scope.vendor_total_amount_flag = false;
    $scope.error_flag = false;
    $scope.messages = '';
    $scope.init = function(csrf_token) {

        $scope.csrf_token = csrf_token;
        new Picker.Date($$('#start_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
        new Picker.Date($$('#end_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
        
        $scope.get_vendors();

    }
    $scope.get_vendors = function() {
        $http.get('/vendor/list/').success(function(data)
        {
            $scope.vendors = data.vendors;
            $scope.vendor_name = 'select';
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    $scope.set_report_type = function(){
        if($scope.report_name == 'date'){
            $scope.report_date_wise = true;
            $scope.report_vendor_wise = false;
        } else if($scope.report_name == 'vendor'){
             $scope.report_date_wise = false;
             $scope.report_vendor_wise = true;
        }
    }

    $scope.get_report = function(){
        if($scope.report_name == 'date') {
            $scope.report_date_wise_flag = true;
            $scope.report_vendor_wise_flag = false;
        } else if ($scope.report_name == 'vendor') {
            $scope.report_date_wise_flag = false;
            $scope.report_vendor_wise_flag = true;
        }
    }
    $scope.view_report = function(report_type) {
        $scope.report_type = report_type;
        $scope.start_date = $$('#start_date')[0].get('value');
        $scope.end_date = $$('#end_date')[0].get('value');
        if ($scope.report_type == 'date') {
            if ($scope.start_date == '' || $scope.start_date == undefined ){
                $scope.error_flag = true;
                $scope.messages = 'Please choose Start date';
            } else if($scope.end_date == '' || $scope.end_date == undefined ){
                $scope.error_flag = true;
                $scope.messages = 'Please choose End date';
            } else {
               $http.get('/reports/purchase/?report_name=date&start_date='+$scope.start_date+'&end_date='+$scope.end_date).success(function(data){
                    var total_amount = 0;
                    if (data.purchases.length > 0) {
                        $scope.date_total_amount_flag = true;
                        $scope.vendor_total_amount_flag = false;
                    }
                    for (i=0; i < data.purchases.length; i++) {
                        total_amount = parseFloat(total_amount) + parseFloat(data.purchases[i].amount);
                        data.purchases[i].amount = data.purchases[i].amount.toFixed(2);
                    }
                    $scope.purchases = data.purchases;
                    
                    $scope.purchase_amount_total = total_amount.toFixed(2);
                }); 
            }
       } else {
            if ($scope.vendor_name == '' || $scope.vendor_name == undefined || $scope.vendor_name == 'select') {
                $scope.error_flag = true;
                $scope.messages = 'Please choose Vendor';
            } else {
                $http.get('/reports/purchase/?report_name=vendor&vendor_name='+$scope.vendor_name).success(function(data){
                    if (data.purchases.length > 0) {
                        $scope.date_total_amount_flag = false;
                        $scope.vendor_total_amount_flag = true;
                    }
                    var total_amount = 0;
                    for (i=0; i < data.purchases.length; i++) {
                        total_amount = parseFloat(total_amount) + parseFloat(data.purchases[i].amount);
                        data.purchases[i].amount = data.purchases[i].amount.toFixed(2);
                    }
                    $scope.purchases_vendor = data.purchases;
                    
                    $scope.purchase_amount_total = total_amount.toFixed(2);
                });
                
            }
       }
        
    } 
}

function ExpenseReportController($scope, $http, $element, $timeout, $location){

    $scope.start_date = '';
    $scope.end_date = '';

    $scope.expense_total_amount_flag = false;
    $scope.error_flag = false;
    $scope.messages = '';

    $scope.init = function(csrf_token) {
        $scope.csrf_token = csrf_token;
        new Picker.Date($$('#start_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
        new Picker.Date($$('#end_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
    }
    $scope.view_report = function() {
        $scope.start_date = $$('#start_date')[0].get('value');
        $scope.end_date = $$('#end_date')[0].get('value');
        if ($scope.start_date == '' || $scope.start_date == undefined ){
            $scope.error_flag = true;
            $scope.messages = 'Please choose Start date';
        } else if($scope.end_date == '' || $scope.end_date == undefined ){
            $scope.error_flag = true;
            $scope.messages = 'Please choose End date';
        } else {
            $http.get('/reports/expenses/?start_date='+$scope.start_date+'&end_date='+$scope.end_date).success(function(data){
                var total_amount = 0;
                if (data.expenses.length > 0) {
                    $scope.expense_total_amount_flag = true;
                }
                for (i=0; i < data.expenses.length; i++) {

                    total_amount = parseFloat(total_amount) + parseFloat(data.expenses[i].amount);
                    data.expenses[i].amount =  data.expenses[i].amount.toFixed(2) ;
                }
                $scope.expenses = data.expenses;
                
                $scope.expense_total_amount = total_amount.toFixed(2);
            }); 
        }      
    } 
}

function PurchaseAccountReportController($scope, $element, $http, $location) {
    $scope.report_name = 'date';
    $scope.start_date = '';
    $scope.end_date = '';
    $scope.report_type = '';
    $scope.vendor_name = 'select';
    $scope.report_date_wise_flag = true;
    $scope.report_vendor_wise_flag = false;
    $scope.error_flag = false;
    $scope.messages = ' ';
    $scope.init = function(csrf_token) {

        $scope.csrf_token = csrf_token;
        new Picker.Date($$('#start_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
        new Picker.Date($$('#end_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
        
        $scope.get_vendors();

    }
    $scope.get_vendors = function() {
        $http.get('/vendor/list/').success(function(data)
        {
            $scope.vendors = data.vendors;
            $scope.vendor_name = 'select';
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }

    $scope.get_report = function(){
        if($scope.report_name == 'date') {
            $scope.report_date_wise_flag = true;
            $scope.report_vendor_wise_flag = false;
        } else if ($scope.report_name == 'vendor') {
            $scope.report_date_wise_flag = false;
            $scope.report_vendor_wise_flag = true;
        }
    }
    $scope.view_report = function(report_type) {
        $scope.report_type = report_type;
        $scope.start_date = $$('#start_date')[0].get('value');
        $scope.end_date = $$('#end_date')[0].get('value');
        if ($scope.report_type == 'date') {
            if ($scope.start_date == '' || $scope.start_date == undefined ){
                $scope.error_flag = true;
                $scope.messages = 'Please choose Start date';
            } else if($scope.end_date == '' || $scope.end_date == undefined ){
                $scope.error_flag = true;
                $scope.messages = 'Please choose End date';
            } else {
               $http.get('/reports/purchase_accounts/?report_name=date&start_date='+$scope.start_date+'&end_date='+$scope.end_date).success(function(data){
                    for (i=0; i < data.purchase_accounts.length; i++) {
                        data.purchase_accounts[i].total_amount = data.purchase_accounts[i].total_amount.toFixed(2);
                        data.purchase_accounts[i].paid_amount = data.purchase_accounts[i].paid_amount.toFixed(2);
                        data.purchase_accounts[i].balance = data.purchase_accounts[i].balance.toFixed(2);  
                    }
                    $scope.purchase_accounts = data.purchase_accounts;
                }); 
            }
       } else {
            if ($scope.vendor_name == '' || $scope.vendor_name == undefined || $scope.vendor_name == 'select') {
                $scope.error_flag = true;
                $scope.messages = 'Please choose Vendor';
            } else {
                $http.get('/reports/purchase_accounts/?report_name=vendor&vendor_name='+$scope.vendor_name).success(function(data){
                    
                    for (i=0; i < data.purchase_accounts.length; i++) {
                        data.purchase_accounts[i].total_amount = data.purchase_accounts[i].total_amount.toFixed(2);
                        data.purchase_accounts[i].paid_amount = data.purchase_accounts[i].paid_amount.toFixed(2);
                        data.purchase_accounts[i].balance = data.purchase_accounts[i].balance.toFixed(2); 
                    }
                    $scope.purchase_accounts_vendor = data.purchase_accounts;
                });
            }
       }
        
    } 
}

function PurchaseReturnReportController($scope, $element, $http, $location) {
    $scope.report_name = 'date';
    $scope.start_date = '';
    $scope.end_date = '';
    $scope.report_type = '';
    $scope.vendor_name = 'select';
    $scope.report_date_wise_flag = true;
    $scope.report_vendor_wise_flag = false;
    $scope.date_total_amount_flag = false;
    $scope.vendor_total_amount_flag = false;
    $scope.error_flag = false;
    $scope.messages = '';
    $scope.init = function(csrf_token) {

        $scope.csrf_token = csrf_token;
        new Picker.Date($$('#start_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
        new Picker.Date($$('#end_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
        
        $scope.get_vendors();

    }
    $scope.get_vendors = function() {
        $http.get('/vendor/list/').success(function(data)
        {
            $scope.vendors = data.vendors;
            $scope.vendor_name = 'select';
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }

    $scope.get_report = function(){
        if($scope.report_name == 'date') {
            $scope.report_date_wise_flag = true;
            $scope.report_vendor_wise_flag = false;
        } else if ($scope.report_name == 'vendor') {
            $scope.report_date_wise_flag = false;
            $scope.report_vendor_wise_flag = true;
        }
    }
    $scope.view_report = function(report_type) {
        $scope.report_type = report_type;
        $scope.start_date = $$('#start_date')[0].get('value');
        $scope.end_date = $$('#end_date')[0].get('value');
        if ($scope.report_type == 'date') {
            if ($scope.start_date == '' || $scope.start_date == undefined ){
                $scope.error_flag = true;
                $scope.messages = 'Please choose Start date';
            } else if($scope.end_date == '' || $scope.end_date == undefined ){
                $scope.error_flag = true;
                $scope.messages = 'Please choose End date';
            } else {
               $http.get('/reports/purchase_return/?report_name=date&start_date='+$scope.start_date+'&end_date='+$scope.end_date).success(function(data){
                    var total_amount = 0;
                    if (data.purchase_returns.length > 0) {
                        $scope.date_total_amount_flag = true;
                        $scope.vendor_total_amount_flag = false;
                    }
                    // for (i=0; i < data.purchases.length; i++) {
                    //     total_amount = parseFloat(total_amount) + parseFloat(data.purchases[i].amount);
                    //     data.purchases[i].amount = data.purchases[i].amount.toFixed(2);
                    // }
                    // $scope.purchase_returns = data.purchases;
                    
                    // $scope.purchase_amount_total = total_amount.toFixed(2);
                }); 
            }
       } else {
            if ($scope.vendor_name == '' || $scope.vendor_name == undefined || $scope.vendor_name == 'select') {
                $scope.error_flag = true;
                $scope.messages = 'Please choose Vendor';
            } else {
                $http.get('/reports/purchase_return/?report_name=vendor&vendor_name='+$scope.vendor_name).success(function(data){
                    if (data.purchase_returns.length > 0) {
                        $scope.date_total_amount_flag = false;
                        $scope.vendor_total_amount_flag = true;
                    }
                    // var total_amount = 0;
                    // for (i=0; i < data.purchases.length; i++) {
                    //     total_amount = parseFloat(total_amount) + parseFloat(data.purchases[i].amount);
                    //     data.purchases[i].amount = data.purchases[i].amount.toFixed(2);
                    // }
                    // $scope.purchases_vendor = data.purchases;
                    
                    // $scope.purchase_amount_total = total_amount.toFixed(2);
                });
                
            }
       }
        
    } 
}

function StockReportController($scope, $element, $http, $timeout, $location) {
    $scope.init = function(csrf_token) {
        $scope.csrf_token = csrf_token;
        $scope.get_stock();
    }
    $scope.get_stock = function(){
        $http.get('/reports/stock_reports/').success(function(data)
        {
            $scope.stocks = data.stocks;
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
}


function SalesReportController($scope, $element, $http, $timeout, $location){

    $scope.report_date_wise = true;
    $scope.report_item_wise = false;
    $scope.report_customer_wise = false;
    $scope.report_salesman_wise = false; 
    $scope.error_flag = false;   

    $scope.init = function(){ 

        $scope.report_type = 'date';
        $scope.error_flag = false;

        new Picker.Date($$('#start_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
        new Picker.Date($$('#end_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
        new Picker.Date($$('#item_start_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
        new Picker.Date($$('#item_end_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
        new Picker.Date($$('#customer_start_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
        new Picker.Date($$('#customer_end_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
        new Picker.Date($$('#salesman_start_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
        new Picker.Date($$('#salesman_end_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
        
        $scope.get_customers();
        $scope.get_salesman();
    }
    $scope.get_report_type =function() {
        if($scope.report_type == 'date'){
            $scope.error_flag = false;
            $scope.report_date_wise = true;
            $scope.report_item_wise = false;
            $scope.report_customer_wise = false;
            $scope.report_salesman_wise = false;
            
            $scope.sales_report = '';
            $scope.total_sales_report = '';
        }
        else if($scope.report_type == 'item'){
            $scope.error_flag = false;
            $scope.report_date_wise = false;
            $scope.report_item_wise = true;
            $scope.report_customer_wise = false;
            $scope.report_salesman_wise = false;
            
            $scope.sales_report = '';
            $scope.total_sales_report = '';
        }
        else if($scope.report_type == 'customer'){
            $scope.error_flag = false;
            $scope.report_date_wise = false;
            $scope.report_item_wise = false;
            $scope.report_customer_wise = true;
            $scope.report_salesman_wise = false;
            
            $scope.sales_report = '';
            $scope.total_sales_report = '';            
        }
        else if($scope.report_type == 'salesman'){
            $scope.error_flag = false;
            $scope.report_date_wise = false;
            $scope.report_item_wise = false;
            $scope.report_customer_wise = false;
            $scope.report_salesman_wise = true;
            
            $scope.sales_report = '';
            $scope.total_sales_report = '';            
        }        
    }
    $scope.get_customers = function() {
        $http.get('/customer/list/').success(function(data)
        {
            $scope.customers = data.customers;
            $scope.customer_name = 'select';
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    $scope.get_salesman = function() {
        $http.get('/salesman/list/').success(function(data)
        {
            $scope.salesmen = data.salesmen;
            $scope.salesman_name = 'select';
        })
    }
    $scope.view_report = function(report_type){
        $scope.error_flag = false;
        if(report_type == 'date'){
            $scope.start_date = $$('#start_date')[0].get('value');
            $scope.end_date = $$('#end_date')[0].get('value');
            if ($scope.start_date == '' || $scope.start_date == undefined ){
                $scope.error_flag = true;
                $scope.messages = 'Please choose Start date';
            } else if($scope.end_date == '' || $scope.end_date == undefined ){
                $scope.error_flag = true;
                $scope.messages = 'Please choose End date';
            } else{
                $http.get('/reports/sales_reports/?report_name=date&start_date='+$scope.start_date+'&end_date='+$scope.end_date).success(function(data){
                    $scope.sales_report = data['sales_report'];
                    $scope.total_sales_report = data['total_sales_report'][0];
                });
            }
        }
        else if(report_type == 'item'){
            $scope.start_date = $$('#item_start_date')[0].get('value');
            $scope.end_date = $$('#item_end_date')[0].get('value');
            if ($scope.start_date == '' || $scope.start_date == undefined ){
                $scope.error_flag = true;
                $scope.messages = 'Please choose Start date';
            } else if($scope.end_date == '' || $scope.end_date == undefined ){
                $scope.error_flag = true;
                $scope.messages = 'Please choose End date';
            } else{
                $http.get('/reports/sales_reports/?report_name=item&start_date='+$scope.start_date+'&end_date='+$scope.end_date).success(function(data){
                    $scope.sales_report = data['sales_report'];
                    $scope.total_sales_report = data['total_sales_report'][0];
                });
            }
        }
        else if(report_type == 'customer'){
            $scope.start_date = $$('#customer_start_date')[0].get('value');
            $scope.end_date = $$('#customer_end_date')[0].get('value'); 
            if ($scope.start_date == '' || $scope.start_date == undefined ){
                $scope.error_flag = true;
                $scope.messages = 'Please choose Start date';
            } else if($scope.end_date == '' || $scope.end_date == undefined ){
                $scope.error_flag = true;
                $scope.messages = 'Please choose End date';
            } else if($scope.customer_name == '' || $scope.customer_name == 'select'){
                $scope.error_flag = true;
                $scope.messages = 'Please choose Customer';
            } else{           
                $http.get('/reports/sales_reports/?report_name=customer&customer_name='+$scope.customer_name+'&start_date='+$scope.start_date+'&end_date='+$scope.end_date).success(function(data){
                    $scope.sales_report = data['sales_report'];
                    $scope.total_sales_report = data['total_sales_report'][0];
                });
            }
        }
        else if(report_type == 'salesman'){
            $scope.start_date = $$('#salesman_start_date')[0].get('value');
            $scope.end_date = $$('#salesman_end_date')[0].get('value');
            if ($scope.start_date == '' || $scope.start_date == undefined ){
                $scope.error_flag = true;
                $scope.messages = 'Please choose Start date';
            } else if($scope.end_date == '' || $scope.end_date == undefined ){
                $scope.error_flag = true;
                $scope.messages = 'Please choose End date';
            } else if($scope.salesman_name == '' || $scope.salesman_name == 'select'){
                $scope.error_flag = true;
                $scope.messages = 'Please choose Salesman';
            } else{

                $http.get('/reports/sales_reports/?report_name=salesman&salesman_name='+$scope.salesman_name+'&start_date='+$scope.start_date+'&end_date='+$scope.end_date).success(function(data){
                    $scope.sales_report = data['sales_report'];
                    $scope.total_sales_report = data['total_sales_report'][0];
                });
            }
        }        
    }
}

function PurchaseReturnController($scope, $element, $http, $timeout, share, $location) {
    $scope.purchase_return = {
        'purchase_return_date': '',
        'invoice_number': '',
        'purchase_items': []

    }
    $scope.init = function(csrf_token, invoice_number) {
        $scope.csrf_token = csrf_token;
        $scope.purchase_return.invoice_number = invoice_number;
        new Picker.Date($$('#purchase_return_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
    }
  
    $scope.load_purchase = function() {
        var invoice = $scope.purchase.purchase_invoice_number;
        $http.get('/purchase/?invoice_no='+$scope.purchase.purchase_invoice_number).success(function(data)
        {
            $scope.selecting_item = true;
            $scope.item_selected = false;
            $scope.purchase = data.purchase;
            $scope.purchase.deleted_items = [];
            $scope.purchase.purchase_invoice_number = invoice;
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    $scope.addReturnItems = function(item) {
        var ind = $scope.purchase_return.purchase_items.indexOf(item)
        if(ind >= 0 && !item.selected){
            $scope.purchase_return.purchase_items.splice(ind, 1);
        } else if(item.selected) {
            $scope.purchase_return.purchase_items.push(item);
            var i = $scope.purchase_return.purchase_items.indexOf(item);
        }
        
    }
    $scope.calculate_return_amount = function(item){
        item.returned_amount = parseFloat(item.returned_quantity) * parseFloat(item.cost_price);
        $scope.calculate_net_return_amount();
    }
    $scope.calculate_net_return_amount = function() {
        var amount = 0;
        for(var i=0;i<$scope.purchase_return.purchase_items.length;i++) {
            amount = amount + $scope.purchase_return.purchase_items[i].returned_amount;
        }
        $scope.purchase_return.net_return_total = amount;
    }
    $scope.save_purchase_return = function() {
        $scope.purchase_return.purchase_invoice_number = $scope.purchase.purchase_invoice_number;
        for(var i=0; i< $scope.purchase_return.purchase_items.length; i++){
            $scope.purchase_return.purchase_items[i].selected = "selected";
        }
        if($$('#purchase_return_date')[0].get('value') == '') {
            $scope.validation_error = "Please select date";
            return false;
        }
        $scope.purchase_return.purchase_return_date = $$('#purchase_return_date')[0].get('value');
        params = {
            "csrfmiddlewaretoken" : $scope.csrf_token,
            'purchase_return': angular.toJson($scope.purchase_return),
        }
        $http({
            method : 'post',
            url : "/purchase/return/",
            data : $.param(params),
            headers : {
                'Content-Type' : 'application/x-www-form-urlencoded'
            }
        }).success(function(data, status) {
            document.location.href = '/purchase/entry/';
           
        }).error(function(data, success){
            
        });
    }
}

function SalesReturnReportController($scope, $element, $http, $timeout, $location){

    $scope.error_flag = false;

    $scope.init = function(){ 
        $scope.error_flag = false;      
        new Picker.Date($$('#start_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
        new Picker.Date($$('#end_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
    }
    $scope.view_report = function(){
        $scope.error_flag = false;
        $scope.start_date = $$('#start_date')[0].get('value');
        $scope.end_date = $$('#end_date')[0].get('value');
        if ($scope.start_date == '' || $scope.start_date == undefined ){
            $scope.error_flag = true;
            $scope.messages = 'Please choose Start date';
        } else if($scope.end_date == '' || $scope.end_date == undefined ){
            $scope.error_flag = true;
            $scope.messages = 'Please choose End date';
        } else {
    
            $http.get('/reports/salesreturn_reports/?start_date='+$scope.start_date+'&end_date='+$scope.end_date).success(function(data){
                          
                $scope.salesreturn_report = data['salesreturn_report'];
                $scope.salesreturn_report_total = data['salesreturn_report_total'][0];
                
            });
        }
    }


}

function SalesReturnController($scope, $element, $http, $timeout, share, $location) {
    
    $scope.sales_return = {
        'invoice_number': '',
        'sales_return_date': '',
        'net_amount': '',
        'sales_items': [],
    }
    $scope.init = function(csrf_token, invoice_number){
        $scope.csrf_token = csrf_token;
        $scope.sales_return.invoice_number = invoice_number;
        new Picker.Date($$('#sales_return_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
    }
    $scope.getItems = function(parameter) {
        $scope.items = [];
        $scope.selecting_item = true;
        $scope.item_selected = false;
        console.log('in get items', parameter);
        for(var i=0; i<$scope.sales.sales_items.length; i++){
            if(parameter == 'item_code') {
                if($scope.item_code == ''){
                    $scope.items = [];
                }
                if($scope.sales.sales_items[i].item_code.indexOf($scope.item_code) == 0) {
                    $scope.items.push($scope.sales.sales_items[i]);
                } else {
                    var ind = $scope.items.indexOf($scope.sales.sales_items[i]);
                    if(ind > 0){
                        $scope.items.splice($scope.sales.sales_items[i], 1);
                    }
                }
            }
            if(parameter == 'item_name') {
                if($scope.item_name == ''){
                    $scope.items = [];
                }
                if($scope.sales.sales_items[i].item_name.indexOf($scope.item_name) == 0) {
                    $scope.items.push($scope.sales.sales_items[i]);
                } else {
                    var ind = $scope.items.indexOf($scope.sales.sales_items[i]);
                    if(ind > 0){
                        $scope.items.splice($scope.sales.sales_items[i], 1);
                    }
                }
            }
            if(parameter == 'barcode') {
                if($scope.barcode == ''){
                    $scope.items = [];
                }
                if($scope.sales.sales_items[i].barcode.indexOf($scope.barcode) == 0) {
                    $scope.items.push($scope.sales.sales_items[i]);
                } else {
                    var ind = $scope.items.indexOf($scope.sales.sales_items[i]);
                    if(ind > 0){
                        $scope.items.splice($scope.sales.sales_items[i], 1);
                    }
                }
            }
        }

    }
    $scope.load_sales = function() {
        var invoice = $scope.sales.sales_invoice_number;
        $http.get('/sales/?invoice_no='+$scope.sales.sales_invoice_number).success(function(data)
        {
            $scope.selecting_item = true;
            $scope.item_selected = false;
            $scope.sales = data.sales;
            $scope.sales.deleted_items = [];
            $scope.sales.sales_invoice_number = invoice;
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    
}

function AddItemController($scope, $http, $element, $location, $timeout) {
    
    $scope.brand_value = 'select';
    $scope.brand_name = '';
    $scope.uom_value = 'select';
    $scope.uom_name = '';
    $scope.error_flag = false;
    $scope.is_valid = false;
    $scope.message = '';

    $scope.init = function(csrf_token){

        $scope.csrf_token = csrf_token;
        $scope.get_brands();
        $scope.get_uoms();
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
        if($scope.brand_value == 'other') {
            $scope.error_flag = false;
            $scope.message = '';
            $scope.popup = new DialogueModelWindow({
                'dialogue_popup_width': '27%',
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
                $scope.brand_value = $scope.brand_name;              
            }
        }).error(function(data, success){
            
        });
    }

    $scope.get_uoms = function() {
        $http.get('/inventory/uom_list/').success(function(data)
        {
            $scope.uoms = data.uoms;
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    $scope.add_uom = function() {
        if($scope.uom_value == 'other') {
            $scope.error_flag = false;
            $scope.message = '';
            $scope.popup = new DialogueModelWindow({
                'dialogue_popup_width': '27%',
                'message_padding': '0px',
                'left': '28%',
                'top': '150px',
                'height': '115px',
                'content_div': '#add_uom'
            });
            var height = $(document).height();
            $scope.popup.set_overlay_height(height);
            $scope.popup.show_content();

        }
    }

    $scope.add_new_uom = function() {
        params = { 
            'uom_name':$scope.uom_name,
            "csrfmiddlewaretoken" : $scope.csrf_token
        }
        $http({
            method : 'post',
            url : "/inventory/add/uom/",
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
                $scope.get_uoms();
                $scope.uom_value = $scope.uom_name;              
            }
        }).error(function(data, success){
            
        });
    }
    $scope.form_validation = function(){
        if ($scope.item_name == '' || $scope.item_name == undefined) {
            $scope.error_flag=true;
            $scope.message = 'Item name cannot be null';
            return false;
        } else if($scope.item_code == '' || $scope.item_code == undefined) {
            $scope.error_flag=true;
            $scope.message = 'Item code cannot be null';
            return false;
        } else if($scope.uom_value == '' || $scope.uom_value == undefined || $scope.uom_value == 'select' || $scope.uom_value == 'other') {
            $scope.error_flag=true;
            $scope.message = 'Please choose Uom';
            return false;
        } else if($scope.brand_value == '' || $scope.brand_value == undefined || $scope.brand_value == 'select' || $scope.brand_value == 'other') {
            $scope.error_flag=true;
            $scope.message = 'Please choose Brand';
            return false;
        }else if($scope.bar_code == '' || $scope.bar_code == undefined) {
            $scope.error_flag=true;
            $scope.message = 'Barcode cannot be null';
            return false;
        } else if($scope.tax == '' || $scope.tax == undefined) {
            $scope.error_flag=true;
            $scope.message = 'Tax cannot be null';
            return false;
        }
        return true;
    }
    $scope.save_item = function() {
        $scope.is_valid = $scope.form_validation();
        if ($scope.is_valid) {
            $scope.error_flag=false;
            $scope.message = '';
            params = { 
                'name':$scope.item_name,
                'code': $scope.item_code,
                'brand': $scope.brand_value,
                'barcode': $scope.bar_code,
                'tax': $scope.tax,
                'description': $scope.item_description,
                'uom': $scope.uom_value,
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            $http({
                method : 'post',
                url : "/inventory/add_item/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                
                if (data.result == 'error'){
                    $scope.error_flag=true;
                    $scope.message = data.message;
                } else {
                    $scope.error_flag=false;
                    $scope.message = '';
                    document.location.href = '/';
                }
            }).error(function(data, status){
                $scope.error_flag=true;
                $scope.message = data.message;
            });
        }
    }
    $scope.close_popup = function(){
        $scope.popup.hide_popup();
    }
}


