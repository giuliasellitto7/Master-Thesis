
import pyreadr
import os
import utils
import utils_data_preparation

utils.welcome()

app = utils_data_preparation.ask_user_to_choose_project()

vulmovement_dir = utils.get_path("vulmovement_" + app)
r_metrics_dir = utils.get_path("my_filemetrics_r_" + app)
output_dir = utils.get_path("my_filemetrics_csv_"+app)

utils_data_preparation.check_output_directory(output_dir)

print("Starting task...")

# extract the vulmovement data frame from file
obj = pyreadr.read_r(os.path.join(vulmovement_dir, "vulmovement_" + app + ".Rda"))
vulmovement = obj["vulmovement"]

for version in vulmovement.columns:

    # store vulnerable files names
    vulnerable_files = []
    for filename in vulmovement[version]:
        if filename:
            vulnerable_files.append(filename)

    try:
        # extract the file metrics dataframe from file
        obj = pyreadr.read_r(os.path.join(r_metrics_dir, "RELEASE_" + version + ".Rda"))
        metrics_df = obj["metrics"]

        # build data frame column to store each file's vulnerability label
        # first build an all-NEUTRAL column
        metrics_df["IsVulnerable"] = ["no"] * len(metrics_df.index)

        # add VULNERABLE label to rows corresponding to vulnerable files
        metrics_df.loc[vulnerable_files, ["IsVulnerable"]] = "yes"

        # save metrics with labels in a new file
        metrics_df.to_csv(os.path.join(output_dir, "RELEASE_" + version + ".csv"))

    except pyreadr.custom_errors.PyreadrError:
        # not all versions metrics are stored
        continue

print("Done.")

utils.bye()
