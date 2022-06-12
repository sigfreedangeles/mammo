$(document).ready(function(){
	
	$('#saveMammogram').click(function(){
		console.log('CLICKED SAVE MAMMOGRAM');
		
		var idMammogram = $('#idMammogram').attr('value');
		console.log('ID of mammogram: ' + idMammogram);
		event.preventDefault();
		var title = $('#title').val();
		if (title == ''){
			$('#title').html('Unlabeled');
			title = 'Unlabeled';
		}
		var patientName = $('#patientName').val();
		if (patientName == ''){
			$('#patientName').html('Unregistered');
			patientName = 'Unregistered';
		}
		var breast = $('input[name="breast"]:checked').val();
		var breastView = $('input[name="breastView"]:checked').val();
		var notes = $('#notes').val();
		if (notes == ''){
			$('#notes').html('No description given.');
			notes = 'No description given.';
		}
		var formData = $('#mammogramData').serialize();
		console.log('Title: ' + title + ' patient name: ' + patientName + ' breast: ' + breast + ' breast view: ' + breastView + ' notes: ' + notes);
		
		$.ajax({
			type: 'POST',
			url: '/saveMammogram',
			data: formData,
			success: function(response){
				console.log('saved mammogram data');
				$('#card_' + idMammogram + '_title').html(title);
				$('#card_' + idMammogram + '_patientName').html('Patient name: ' + patientName);
				$('#card_' + idMammogram + '_breast').html('Breast: ' + breast);
				$('#card_' + idMammogram + '_breastView').html('Mammogram view: ' + breastView);
				$('#card_' + idMammogram + '_notes').html('Description: ' + notes);
				$('#mammogramData')[0].reset();
			},
			error: function(response){
				console.log('cannot save mammogram data');
			}
		});
	
	});
	
});