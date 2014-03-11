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
            console.log(data);
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
                'height': 200,
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
    $scope.selecting_item = false;
    $scope.item_selected = false;
    $scope.purchase_items = [];
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
            'qty_purchased': '',
            'cost_price': '',
            'permit_disc_amt': '',
            'permit_disc_percent': '',
            'net_amount': '',
            'unit_price': 0,
            'expense': '',
            'expense_unit': 0
        }
        $scope.purchase_items.push(selected_item);
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
    }
    $scope.calculate_cost_price = function(item) {
        if(item.unit_price != '' || item.frieght_unit != '' || item.handling_unit != '' || item.expense_unit != ''){
            item.cost_price = parseFloat(item.unit_price) + parseFloat(item.frieght_unit) + parseFloat(item.handling_unit) + parseFloat(item.expense_unit)
        }
        $scope.calculate_net_amount(item);
    }

    $scope.calculate_net_amount = function(item) {
        if(item.qty_purchased != '' && item.unit_price != ''){
            item.net_amount = (parseFloat(item.qty_purchased)*parseFloat(item.unit_price)) + parseFloat(item.frieght_unit)+ parseFloat(item.handling_unit)+parseFloat(item.expense_unit).toFixed(3);
        }
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
}