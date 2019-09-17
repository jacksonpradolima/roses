import warnings

import matplotlib.pyplot as plt
import pingouin as pg
import rpy2.robjects as robjects
import seaborn as sns
from rpy2.rinterface import RRuntimeWarning
from rpy2.robjects import pandas2ri

from rose.effect_size.vargha_delaney import VD_A_DF
from rose.utils.r_cheatsets import require_r_package

# Filter the warnings from R
warnings.filterwarnings("ignore", category=RRuntimeWarning)

# To use Pandas with R
pandas2ri.activate()

class kruskal_wallis(object):
    def __init__(self, df, val_col: str, group_col: str, sort=True):
        self.df = df
        self.val_col = val_col
        self.group_col = group_col

        if not sort:
            self.df = df.sort_values(by=group_col)

        self.r_dataframe = pandas2ri.py2ri(self.df)

    def apply(self, alpha=0.05, plot=True, filename="kruskal", use_latex=False):
        kruskal = pg.kruskal(dv=self.val_col, between=self.group_col, data=self.df)
        pvalue = kruskal['p-unc'][0]

        if plot:
            chi_squared = kruskal['H'][0]
            degree_freed = kruskal['ddof1'][0]

            p = "< 0.001" if pvalue < 0.001 else (
                "< 0.01" if pvalue < 0.01 else ("< 0.05" if pvalue < 0.05 else (round(pvalue, 3))))

            sns.boxplot(x=self.group_col, y=self.val_col, data=self.df)

            # Jittered BoxPlots
            sns.stripplot(x=self.group_col, y=self.val_col, data=self.df, size=4, jitter=True, edgecolor="gray")

            # Add mean and median lines
            plt.axhline(y=self.df[self.val_col].mean(), color='r', linestyle='--', linewidth=1.5)
            plt.axhline(y=self.df[self.val_col].median(), color='b', linestyle='--', linewidth=2)

            plt.title("")
            plt.suptitle("")
            plt.xlabel(f"\nKruskal-Wallis chi-squared = {chi_squared}, df = {degree_freed}, p = {p}", labelpad=20)
            plt.ylabel('')
            plt.savefig(filename + ('.pgf' if use_latex else '.pdf'), bbox_inches='tight')
            plt.clf()

        # If the Kruskal-Wallis test is significant, a post-hoc analysis can be performed
        # to determine which levels of the independent variable differ from each other level.
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

        kruskal_post_hoc_nemenyi = robjects.r(rposthoc)

        return kruskal_post_hoc_nemenyi(self.r_dataframe.rx2(self.val_col), self.r_dataframe.rx2(self.group_col))