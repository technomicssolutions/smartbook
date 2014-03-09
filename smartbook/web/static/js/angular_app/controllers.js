function HomeController($scope, $element, $http, $timeout, share, $location)
{
  
}

function ExpenseController($scope, $element, $http, $timeout, share, $location) {

	$scope.expense_heads = [];
	$scope.expense_head = '';

	$scope.init = function(csrf_token)
    {
        $scope.csrf_token = csrf_token;
        $scope.get_expense_head_list();
    }
    $scope.get_expense_head_list = function() {
    	 $http.get('/expenses/get_expense_head_list/').success(function(data)
        {
        	$scope.expense_heads = data.expense_heads;
            $scope.expense_head = 'select';
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    $scope.selected_head = function(head_name) {
    	alert('hii');
    	console.log(head_name);
    	$scope.expense_head = head_name;
    }
	
}