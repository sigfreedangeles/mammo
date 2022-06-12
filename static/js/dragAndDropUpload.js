$(document).ready(function(){
	var lastTarget = null;
	
	var showDropZone = function(event){
		event.preventDefault();
		lastTarget = event.target;
		$('.dropzone').css({'visibility': 'visible', 'opacity': '1'});
	};
	
	var hideDropZone = function(event){
		event.preventDefault();
		if(event.target === lastTarget || event.target === document){
			$('.dropzone').css({'visibility': 'hidden', 'opacity': '0'});
		}
	};
	
	var dropZoneHandler = {
		dragenter: showDropZone,
		dragleave: hideDropZone
	};
	
	$(window).on(dropZoneHandler);
	
	var dragHandler = function(event){
        event.preventDefault();
    };

    var dropHandler = function(event){
        event.preventDefault();
        var imagesToUpload = event.originalEvent.dataTransfer.files;
        console.log(imagesToUpload);
		$('.dropzone').css({'visibility': 'hidden', 'opacity': '0'});
		
		var formData = new FormData();
		$.each(imagesToUpload, function(i, file){
			formData.append('file', file)
		});
		
		$.ajax({
			url : '/predict',
			method : 'post',
			processData : false,
			contentType : false,
			data: formData,
			success: function(json){
				console.log(json);
				$('#imageGallery').append(json);
				console.log($('#imageGallery').html());
				$('#imageGallery').fadeIn(2000);
			},
			error: function(errorMessage){
				console.log(errorMessage);
			}
		});
    };

    var dropHandlerSet = {
        dragover: dragHandler,
        drop: dropHandler
    };

    $('.dropzone').on(dropHandlerSet);
});