$(document).ready(function(){
	$('#workproject').click(function(){
		$('#selectprojecttorun').modal({
			backdrop: 'static',
			keyboard: false
		});		
		$("#selectprojecttorun").on("shown.bs.modal", function () {
			$('#runprojectForm')[0].reset();
			$('.modal-title').html("<i class='fa fa-plus'></i>Select Project To Work On");
			$('#action').val('workproject');
			$('#Select').val('Select');
		});
	});

	$('#viewproject').click(function(){
        $('#selectprojecttoview').modal({
            backdrop: 'static',
            keyboard: false
        });
        $("#selectprojecttoview").on("shown.bs.modal", function () {
            $('#viewprojectForm')[0].reset();
            $('.modal-title').html("<i class='fa fa-plus'></i>Select Project To View Test Cases");
            $('#action').val('viewprojectForm');
            $('#viewproj').val('View Test Cases');
        });
    });

//    $('#upload_csv_file').click(function(){
//        $('#selectfiletoupload').modal({
//            backdrop: 'static',
//            keyboard: false
//        });
//        $("#selectfiletoupload").on("shown.bs.modal", function () {
//            $('#uploadCsvForm')[0].reset();
//            $('.modal-title').html("<i class='fa fa-plus'></i>Choose File CSV To Upload");
//            $('#action').val('uploadCsvForm');
//            $('#UploadCsv').val('Upload CSV');
//        });
//    });
});