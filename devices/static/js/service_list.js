$(function () {

$(".btn-danger").on('click', function(e) {
    var name = $(this).closest('tr').children()[0].innerText,
    	request = {};

    request["name"] = name;

    swal({
        title: "Вы уверены?",
        text: "Сервис " + String(name) + " будет безвозвратно удален!",
        type: "warning",
        confirmButtonColor: "#DD6B55",
        showCancelButton: true,
        confirmButtonText: "Удалить",
        cancelButtonText: "Отмена",
        closeOnConfirm: false
        }, 
    	function(){
			$.post(URL, request, function (response) {
                if (response["text"] === 'success') {
                    swal({
                    	title: "Успешно!",
                    	text: "Сервис " + String(name) + " удален.",
                    	type: "success",
                    	closeOnConfirm: false
                    },
                    function(){
                    	location.href = URL;
                    });
                } else {
                    sweetAlert("Ошибка", "Не удалось удалить сервис", "error");
                }
		    });	 
    });   
});

});