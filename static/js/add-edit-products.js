$(document).ready(function(){
	/** Upload Product toast */
	$('#productForm').submit(function(event){
		event.preventDefault();
		var formData = new FormData(this);

		url = '/product_upload'
		fetch(url, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrftoken
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                toastr.success('Product added successfully! Redirecting in 5 seconds...');
                setTimeout(function() {
                    window.location.href = '/shop';
                }, 5000);
            } else {
                toastr.error('Failed to add product');
            }
        })
        .catch(() => {
            toastr.error('An error occurred');
        });
	});

	/** update product toast */
	$('#productEditForm').submit(function(event){
		event.preventDefault();
		var formData = new FormData(this);

		var url = $(this).attr('action');
		console.log(url)
		fetch(url, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrftoken
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                toastr.success('Product updated successfully! Redirecting in 5 seconds...');
                setTimeout(function() {
                    window.location.href = '/shop';
                }, 5000);
            } else {
                toastr.error('Failed to add product');
            }
        })
        .catch(() => {
            toastr.error('An error occurred');
        });
	});
});