import warnings

import matplotlib.pyplot as plt
import pingouin as pg
import seaborn as sns


import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri

from rpy2.robjects.conversion import localconverter

from roses.effect_size.vargha_delaney import VD_A_DF
from roses.utils.r_cheatsets import require_r_package

# Filter the warnings from R
from rpy2.rinterface import RRuntimeWarning
warnings.filterwarnings("ignore", category=RRuntimeWarning)

# To use Pandas with R
# pandas2ri.activate()


class kruskal_wallis(object):

    def __init__(self, df, val_col: str, group_col: str, sort=True):
        self.df = df
        self.val_col = val_col
        self.group_col = group_col

        if not sort:
            self.df = df.sort_values(by=group_col)

        with localconverter(ro.default_converter + pandas2ri.converter):
            self.r_dataframe = ro.conversion.py2rpy(self.df)

    def apply(self, ax, alpha=0.05, plot=True, ylabel=''):
        kruskal = pg.kruskal(
            dv=self.val_col, between=self.group_col, data=self.df)

        if 'p-unc' in kruskal.columns:
            pvalue = kruskal['p-unc'][0]

            if plot:
                chi_squared, degree_freed = kruskal[
                    'H'][0], kruskal['ddof1'][0]

                p = "< 0.001" if pvalue < 0.001 else (
                    "< 0.01" if pvalue < 0.01 else ("< 0.05" if pvalue < 0.05 else (round(pvalue, 3))))

                sns.boxplot(x=self.group_col, y=self.val_col,
                            data=self.df, ax=ax)

                # Jittered BoxPlots
                sns.stripplot(x=self.group_col, y=self.val_col,
                              data=self.df, size=4, jitter=True, edgecolor="gray", ax=ax)

                # Add mean and median lines
                ax.axhline(y=self.df[self.val_col].mean(),
                           color='r', linestyle='--', linewidth=1.5)
                ax.axhline(y=self.df[self.val_col].median(),
                           color='b', linestyle='--', linewidth=2)

                ax.set_ylabel(ylabel)
                ax.set_xlabel(f"\nKruskal-Wallis p-value = {p}", labelpad=15)

            # If the Kruskal-Wallis test is significant, a post-hoc analysis can be performed
            # to determine which levels of the independent variable differ from
            # each other level.
            if pvalue < alpha:
                return kruskal, [self._post_hoc_nemenyi(), VD_A_DF(self.df, self.val_col, self.group_col)]

        return kruskal, None

    def _post_hoc_nemenyi(self):
        """
        Nemenyi test for multiple comparisons
        Zar (2010) suggests that the Nemenyi test is not appropriate for groups with unequal numbers of observations.
        :return:
        """

        rposthoc = """kruskal.post.hoc <- function(value, group, alpha = 0.05){{
                {0}
                {1}
                {2}                            
                group <- as.factor(group)
                post.results <- tryCatch({{ 
                  kwAllPairsNemenyiTest(value, group, "Tukey")
                }}, warning=function(w) {{      
                  kwAllPairsNemenyiTest(value, group, "Chisquare")
                }})

                ## print("============================= POST-HOC TESTS =============================")                

                ## LaTeX formated: Significances highlighted in bold
                ## Pay attention! Read from left to right the comparations. See the TRUE values!!!
                ##no.diff <- post.results$p.value < alpha
                ##no.diff[is.na(no.diff)] <- FALSE
                ##writeTabular(table=post.results$p.value, format='f', bold=no.diff,hrule=0,vrule=0)

                return(post.results)
            }}
            """.format(require_r_package("PMCMRplus"), require_r_package("devtools"), require_r_package("scmamp"))

        kruskal_post_hoc_nemenyi = ro.r(rposthoc)

        return kruskal_post_hoc_nemenyi(self.r_dataframe.rx2(self.val_col), self.r_dataframe.rx2(self.group_col))
