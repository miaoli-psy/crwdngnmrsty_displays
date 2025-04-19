# 得到sector raw display 后，查看每一种条件下（angle, direction, radial/tan）
# 的numerosity distribution


library(ggplot2)
library(dplyr)
library(stringr)
library(tidyr)
library(purrr)


setwd("d:/OneDrive/Programming/crwdngnmrsty_displays/src/cal_num_distribution/")


csv_folder <- "D:/OneDrive/projects/numerosity_closing_gap/displays/displays_n5000"
csv_files <- list.files(path = csv_folder, pattern = "\\.csv$", full.names = TRUE)

# Extract clean names (remove path & .csv extension)
csv_names <- tools::file_path_sans_ext(basename(csv_files))


# Read and plot each CSV
for (i in seq_along(csv_files)) {
  df_name <- csv_names[i]
  df <- read.csv(csv_files[i])
  assign(df_name, df)
  
  # Count numerosity and calculate percent
  df_summary <- df %>%
    count(numerosity) %>%
    mutate(percent = n / sum(n) * 100)
  
  # Create ggplot bar chart with percentage labels and fixed y-axis
  p <- ggplot(df_summary, aes(x = factor(numerosity), y = percent)) +
    geom_bar(stat = "identity", fill = "skyblue") +
    geom_text(aes(label = paste0(round(percent, 1), "%")), vjust = -0.5) +
    labs(
      title = paste("Numerosity Distribution -", df_name),
      x = "Numerosity",
      y = "Percentage (%)"
    ) +
    ylim(0, 100) +
    theme_minimal()
  
  assign(paste0(df_name, "_plot"), p)
}

# Display all plots
for (name in ls(pattern = "_plot$")) {
  print(get(name))
}


# check numerosity distribution in one df
summary_list <- list()

for (file in csv_files) {
  file_name <- tools::file_path_sans_ext(basename(file))
  
  df <- read.csv(file)
  
  # Parse metadata from file name
  arrangement <- ifelse(str_detect(file_name, "radial"), "radial", "tangential")
  angle <- stringr::str_extract(file_name, "angle(\\d+)") %>% str_remove("angle") %>% as.integer()
  direction <- stringr::str_extract(file_name, "drctn(\\d+)") %>% str_remove("drctn") %>% as.integer()
  
  df_summary <- df %>%
    count(numerosity, name = "n") %>%
    mutate(percent = round(n / sum(n) * 100, 1)) %>%
    arrange(desc(percent))
  
  summary_list[[file_name]] <- tibble(
    source = file_name,
    arrangement = arrangement,
    angle = angle,
    direction = direction,
    numerosity = list(df_summary$numerosity),
    percentage = list(df_summary$percent)
  )
}

numerosity_distribution_df <- bind_rows(summary_list)
