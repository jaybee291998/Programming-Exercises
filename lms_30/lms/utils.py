# helper function
# check if the file being uploaded already exist in the uploaded files
def check_duplicate_file(existing_files, uploaded_file):
	is_duplicate = False
	uploaded_file_name = uploaded_file.name.split('.')[0].replace(' ','_')
	uploaded_file_extention = uploaded_file.name.split('.')[-1]
	for existing_file in existing_files:
		existing_file_name = existing_file.file.name
		existing_file_extention = existing_file_name.split('.')[-1]
	 	# check if the uploaded has the same name in the existing file
		if uploaded_file_name in existing_file_name:
	 		# check if they are the same content type
	 		if uploaded_file_extention == existing_file_extention:
	 			# check if they have the same size
	 			if uploaded_file.size == existing_file.file.size:
	 				# they are the same
	 				return True
	return is_duplicate


# helper function
def byte_to_mb(size_in_bytes):
	return size_in_bytes/(1024**2)

def mb_to_bytes(size_in_mb):
	return size_in_mb*(1024**2)