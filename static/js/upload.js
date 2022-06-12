$(document).ready(function(){
	
	$('#uploadImages').unbind().click(function(event) {
		
		event.preventDefault();
		$('#uploadForm').click();
		
		$('input[name=uploadImagesForm]').unbind().change(function(event) {
			var files = event.target.files;
			console.log(files);
			var formData = new FormData();
			// Loop through each of the selected files.
			for (var i = 0; i < files.length; i++) {
				var file = files[i];
				// Add the file to the request.
				formData.append('file', file);
			}
			
			$.ajax({
				type: 'POST',
				url: '/predict',
				data: formData,
				dataType: 'json',
				processData: false,
				contentType: false,
				success: function(json){
					console.log(json);
					var imageGallery = $('#imageGallery');
					$(imageGallery).append(json);
					console.log(imageGallery.html());
					$(imageGallery).fadeIn(2000);
				},
				error: function(errorMessage){
					console.log(errorMessage);
				}
				
			});
			
			
		});
		
	});
	
});