import warnings

import numpy as np
import pandas as pd
import rpy2.robjects as robjects
from rpy2.rinterface import RRuntimeWarning
from rpy2.robjects import pandas2ri

from roses.utils.r_cheatsets import require_r_package

# Filter the warnings from R
warnings.filterwarnings("ignore", category=RRuntimeWarning)

# To use Pandas with R
pandas2ri.activate()

class friedman(object):
    def __init__(self, filename, val_col: str, group_col: str, instance_col: str):
        """

        :param df: pandas DataFrame object
        :param val_col: Name of the column that contains values (fitness values).
        :param group_col: Name of the column that contains group names (algorith namess).
        :param instance_col: Name of the column that contains instance names (problem names).
        """

        self.df = pd.read_csv(filename, ";")
        self.filename = filename
        self.val_col = val_col
        self.group_col = group_col
        self.instance_col = instance_col

        self.r_dataframe = pandas2ri.py2ri(self.df)

    def apply(self, alpha=0.05, instance_col: str = "Instance"):
        rfriedman = """friedman.test.rose <- function(filename, instance_col, alpha = 0.05){{
            {0}                        
            #read the data
            data <- read.csv(filename, sep=";")
            #remove the Instance column
            data <- data[,!(names(data) %in% c(instance_col))]
            data <- data.matrix(data)

            pre.results <- friedmanTest(data)
            
            list.to.return <- list(p_value = pre.results$p.value, chi_squared = as.numeric(pre.results$statistic))

            return(list.to.return)                        
        }}    
        """.format(require_r_package("PMCMRplus"), self.filename.replace(".csv", ""))

        friedman_r = robjects.r(rfriedman)

        friedman_result = np.asarray(friedman_r(self.filename, instance_col))

        p_value = friedman_result[0][0]
        chi_squared = friedman_result[1][0]

        friedman_result = [p_value, chi_squared]

        if p_value < alpha:
            return friedman_result, self._post_hoc_nemenyi()

        return friedman_result, None

    def _post_hoc_nemenyi(self, instance_col: str = "Instance"):
        rfriedman = """friedman.post.hoc <- function(filename, instance_col, alpha = 0.05){{
                    {0}                          
                    #read the data
                    data <- read.csv(filename, sep=";")
                    #remove the Instance column
                    data <- data[,!(names(data) %in% c(instance_col))]
                    data <- data.matrix(data)

                    post.results <- posthoc.friedman.nemenyi.test(data)                
                    setEPS()
                    postscript("{1}_plotCD.eps", width = 6.0, height = 3.0)
                    output <- scmamp::plotCD(data, alpha=0.05 )
                    dev.off()

                    return(post.results$p.value)                                                            
                }}    
                """.format(require_r_package("PMCMR"), self.filename.replace(".csv", ""))

        friedman_r = robjects.r(rfriedman)

        return  friedman_r(self.filename, instance_col)


