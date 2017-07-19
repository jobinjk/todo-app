var blobApp = angular.module('blobApp',[],function($interpolateProvider){
    $interpolateProvider.startSymbol("[[");
    $interpolateProvider.endSymbol("]]");
});

blobApp.controller("MainController",['$scope','$http','$window', function($scope,$http,$window){
    // $scope.test_var = "testing scope";
    // $scope.changeText = function(){
    //     $('#testVarH2').text("changed text");

    $scope.tasks = $window.his_tasks;

    $scope.loginForm = function(){
        $http({
            url: '/login',
            method: 'POST',
            data: JSON.stringify({
                'username':$scope.login.username,
                'password':$scope.login.password
            }),
            headers: {'Content-Type':'application/json'}
        }).then(function(response){

            if(response.data['status'] == true){
                $window.location.reload();
            }
            else{

            }
        });
    }

    $scope.signupForm = function(){
        $http({
            url: '/signup',
            method: 'POST',
            data: JSON.stringify({
                'username':$scope.signup.username,
                'password':$scope.signup.password
            }),
            headers: {'Content-Type':'application/json'}
        }).then(function(response){


            if(response.data['status'] == true){
                $window.location.reload();
            }
            else{

            }

        });
    }

    // $scope.logoutForm = function(){
    //     $http({
    //         url: '/logout',
    //         method: 'POST',
    //         headers: {'Content-Type':'application/json'}
    //     }).then(function(response){

    //         if(response.data['status'] == true){
    //             $window.location.reload();
    //         }
    //         else{

    //         }
    //     });
    // }
    $scope.savetaskForm = function(){
        $http({
            url: '/newtask',
            method: 'POST',
            data:JSON.stringify({"task":$scope.taskModel,"description":$scope.descriptionModel,
                    "date_completed":$scope.date_createdModel, "priority":$scope.priorityModel}),
                // JSON is an angular module that takes object string(like dictionary, key value pair) as input and converts it to JSON, which is then assigned to data:
                header:{"Content-Type":"application/json"}
        }).then(function(response) {
            if(response.data.status == true){
                $scope.tasks = response.data.tasks;
                $scope.beforeTasksChanged = angular.copy(response.data.tasks);
                swal('Way to go!','You have added a new task!!','success')
            }
            else{
                swal('Aww poop!',"We couldn't add it for you! Please try again!", 'error')
            }
        })
    }



    $scope.removetaskForm = function(task){
        
            $http({
                url:'/delete',
                method:'POST',
                data:{'task_id':task.task_id},
                headers:{'Content-Type':'application/json'}
                }).then(function(response) {
                if(response.data.status == true){
                    $scope.tasks = response.data.tasks;
                    $scope.beforeTasksChanged = angular.copy(response.data.tasks);
                    swal("Yippee!", "You just completed/deleted a task! Way to go champ!", "success")
                }
                // else{
                    
                    // swal("Aww poop!", "We couldn't delete the task! Please try again!", "error")
                // }
            });
    }
    

    $scope.getTasks = function(filter){
        $http({
            url:'/getTasks',
            method:'get',
            params:{'filter':filter}
        })
        .then(function(response){
                if(response.data.status == true){
                    $scope.tasks = response.data.tasks;
                }
        });
    }

    $scope.showEdit = function(task){
        $("#editForm").modal("show");
        $scope.edit_task = angular.copy(task);

        console.log($scope.edit_task,task);
    }

    $scope.editForm = function(task){
            
                $http({
                    url:'/edit',
                    method:'POST',
                    data:{'task':task},
                    headers:{'Content-Type':'application/json'}
                    }).then(function(response) {
                    if(response.data.status == true){
                        $scope.tasks = response.data.tasks;
                        $scope.beforeTasksChanged = angular.copy(response.data.tasks);
                        swal("Yippee!", "You just editted a task!", "success")
                    }
                    // else{
                        
                        // swal("Aww poop!", "We couldn't delete the task! Please try again!", "error")
                    // }
                });
        }



    $scope.markAsFinished = function(task){
        
            $http({
                url:'/markAsFinished',
                method:'POST',
                data:{'task_id':task.task_id},
                headers:{'Content-Type':'application/json'}
                }).then(function(response) {
                if(response.data.status == true){
                    $scope.tasks = response.data.tasks;
                    $scope.beforeTasksChanged = angular.copy(response.data.tasks);
                    swal("Yippee!", "You just completed a task! Way to go champ!", "success")
                }
                // else{
                    
                    // swal("Aww poop!", "We couldn't delete the task! Please try again!", "error")
                // }
            });
    }


    
}]);