$(document).ready(function(){
	
	var imageForCropping;
	var cropBoxData;
	var canvasData;
	var cropper;
	
	$(document).on('click', 'a.thumbnail, .edit-icon', function(event){
		event.preventDefault();
		console.log(event.target);
		var imageSource = $(event.target.closest('.thumbnail-container'))[0].getAttribute('thumbnail-src');
		var idMammogram = $(event.target.closest('.thumbnail-container'))[0].getAttribute('thumbnail-id');
		console.log('Image loaded: ' + imageSource + ' | id of image: ' + idMammogram);
		console.log(imageSource);
		$('#modalImage').attr('src', imageSource);
		$('#idMammogram').attr('value', idMammogram);
	});
	
	$(document).on('click', '#saveMammogram', function(event){
		event.preventDefault();
		
		cropper.getCroppedCanvas().toBlob(function (blob) {
			var idMammogram = $('#idMammogram').val();
			var formData = new FormData();
			formData.append('croppedFile', blob);
			formData.append('id', idMammogram);
			console.log('ID of mammogram: ' + idMammogram + ' file: ' + blob)
			console.log(formData.get('croppedFile'));

			$.ajax({
				method: 'POST',
				url: '/saveCroppedFile',
				data: formData,
				contentType: false,
				processData: false,
				dataType: 'json',
				success: function (response) {
					console.log('Upload success');
				},
				error: function (response) {
					console.log('Upload error');
				}
			});
		});
	});
	
	$(document).on('shown.bs.modal', '#modal', function () {
		imageForCropping = document.getElementById('modalImage');
		cropper = new Cropper(imageForCropping, {
			viewMode: 1,
			preview: '.preview',
			dragMode: 'move',
			cropBoxMovable: false,
			cropBoxResizable: false,
			movable: true,
			zoomable: false,
			background: false,
			ready: function (e) {
				cropper.setCanvasData({
					width: 500,
					height: 500,
					top: 0,
					left: -50
				});
				cropper.setCropBoxData({
					width: 100,
					height: 100,
					top: 70,
					left: 120
				});
			}
		});
		$(imageForCropping).css('visibility', 'visible');
		$('.preview').css('visibility', 'visible');
		console.log(cropper.getCanvasData().toString());
	}).on('hidden.bs.modal', '#modal', function () {
		cropBoxData = cropper.getCropBoxData();
		canvasData = cropper.getCanvasData();
		cropper.destroy();
	});
	
	
});