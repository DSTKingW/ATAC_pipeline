working_dir=`pwd`
matrix=$1

/gpfs/bin/R-3.5.2/bin/Rscript /gpfs/output/20191124_ATAC_tool_development/bin/TSSscore.R $matrix
