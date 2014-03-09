function HomeController($scope, $element, $http, $timeout, share, $location)
{
  
}

function ExpenseController($scope, $element, $http, $timeout, share, $location) {

	$scope.init = function(csrf_token)
    {
        $scope.csrf_token = csrf_token;
    }
	
}