# 得到sector raw display 后，查看每一种条件下（angle, direction, radial/tan）
# 的numerosity distribution


library(ggplot2)
library(dplyr)


setwd("d:/OneDrive/Programming/crwdngnmrsty_displays/src/cal_num_distribution/")


csv_folder <- "D:/OneDrive/projects/numerosity_closing_gap/displays/displays_n100"
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
  p <- ggplot(df_summary, aes(x = factor(numerosity), y = n)) +
    geom_bar(stat = "identity", fill = "skyblue") +
    geom_text(aes(label = paste0(round(percent, 1), "%")), vjust = -0.5) +
    labs(
      title = paste("Numerosity Distribution -", df_name),
      x = "Numerosity",
      y = "Count"
    ) +
    ylim(0, 100) +
    theme_minimal()
  
  # Save plot object
  assign(paste0(df_name, "_plot"), p)
}

# Display all plots
for (name in ls(pattern = "_plot$")) {
  print(get(name))
}
