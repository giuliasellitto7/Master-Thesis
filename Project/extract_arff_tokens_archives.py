
import gzip
import shutil
import os
import utils
import utils_data_preparation

utils.welcome()

app = utils_data_preparation.ask_user_to_choose_project()

input_dir = utils.get_path("tokens_" + app)
output_dir = utils.get_path("my_tokens_arff_" + app)

utils_data_preparation.check_output_directory(output_dir)

print("Starting task...")

for filename in os.listdir(input_dir):
    archive_filename = os.path.join(input_dir, filename)
    release_str = filename.split("-")[1]
    output_filename = os.path.join(output_dir, "RELEASE_" + release_str + ".arff")

    with gzip.open(archive_filename, 'rb') as f_in:
        with open(output_filename, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

print("Done.")

utils.bye()
