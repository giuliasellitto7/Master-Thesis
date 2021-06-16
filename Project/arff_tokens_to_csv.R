print("INFO SUL PROGRAMMA")

#clean the environment
rm(list = ls())

path_config = read.csv("path_config.csv", header = TRUE, row.names = 1)

print("Please choose app")
app_name = switch(menu(c("Moodle", "PHPMyAdmin")), "moodle", "phpmyadmin")

output_dir_key = paste("my_tokens_csv_", app_name, sep = "")
output_dir = path_config[output_dir_key, "path"]

task = function() {
  print("Starting task...")
  
  input_dir_key = paste("my_tokens_arff_", app_name, sep = "")
  input_dir = path_config[input_dir_key, "path"]
  previous_wd = getwd()
  setwd(input_dir)
  
  library(foreign)
  
  all_input_file_names = list.files()
  
  for(i in 1:length(all_input_file_names)) {
    mydata=read.arff(all_input_file_names[i])
    file_name = strsplit(all_input_file_names[i], ".arff")
    output_file = paste(output_dir, "/", file_name, ".csv", sep = "")
    write.csv(mydata, output_file)
  }
  
  setwd(previous_wd)
  
  print("Done.")
}


if (dir.exists(output_dir)) {
  print("Directory already exists: maybe the task has alredy been executed.")
  print("Do you want to continue? (Duplicate files will be overwritten)")
  switch(menu(c("Yes, continue", "No, exit program")), task(), {})
} else {
  dir.create(output_dir)
  task()
}

#clean the environment
rm(list = ls())

print("Bye!")