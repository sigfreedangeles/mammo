$(document).ready(function(){
	
	$('#deleteAll').unbind().click(function(event) {
		
		event.preventDefault();
		
		$.ajax({
				type: 'POST',
				url: '/deleteAll',
				dataType: 'json',
				processData: false,
				contentType: false,
				success: function(json){
					$('.thumbnail-container').remove();
					console.log('deleted everything');
				},
				error: function(errorMessage){
					console.log('cannot delete everything');
				}
				
			});
		
	});
	
});