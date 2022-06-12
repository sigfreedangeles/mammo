$(document).ready(function(){
	var pdfdoc = new jsPDF();
	
	$('#gpdf').click(function(){
		pdfdoc.fromHTML($('#PDFcontent').html(), 10, 10, {
			'width': 110
		});
		pdfdoc.save('mammogramreport.pdf')
	});
	
});