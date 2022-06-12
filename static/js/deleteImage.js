$(document).ready(function(){
	
	$(document).on('click', '.thumbnail-container .card-body .delete-icon', function(event){
		idMammogram = event.target.closest('.thumbnail-container').getAttribute('thumbnail-id');
		console.log('ID of mammogram to delete: ' + idMammogram);

		$.ajax({
			url : '/delete',
			data : {id: idMammogram},
			type : 'POST',
			success : function(response){
				$('.thumbnail-container[thumbnail-id="' + idMammogram + '"]').remove();
				console.log('success deleted');
			},
			error: function(response){
				console.log('cannot delete image');
			}
		});

	});
	
});