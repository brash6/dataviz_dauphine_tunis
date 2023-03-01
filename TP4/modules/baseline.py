import warnings

import numpy as np
import pandas as pd
from scipy import sparse
from scipy.sparse.linalg import spsolve

# Initialization
warnings.filterwarnings('ignore')
np.seterr(divide='ignore', invalid='ignore')


# ----------------------------------------------------- UTILS ----------------------------------------------------------
# Baseline correction by 2nd derivative constrained weighted regression
def baseline_als(y, lam, p, niter=100):
    """
    Asymmetric least squares smoothing
    https://pubs.rsc.org/en/content/articlehtml/2015/an/c4an01061b

    Iterative algorithm applying 2nd derivative constraints,
    Weights from previous iteration is p for positive residuals and 1-p for negative residuals

    input:
        y: data (matrix with spectra in rows)
        lam: smoothness parameter (2nd derivative constraint)
        p (asymmetry parameter): weighting of positive residuals (and 1-p for negative residuals)
        niter: maximum number of iterations

    output:
        baseline
    """
    L = len(y)
    D = sparse.diags([1, -2, 1], [0, -1, -2], shape=(L, L-2))
    w = np.ones(L)
    for i in range(niter):
        W = sparse.spdiags(w, 0, L, L)     # return a sparse matrix from diagonals
        Z = W + lam * D.dot(D.transpose())
        b = spsolve(Z, w*y)                # solve(A,b) the sparse linear system Ax=b, where b may be a vector or a matrix
        w = p * (y > b) + (1-p) * (y < b)
    return b


class Baseline():
    """
    Inputs:
        - df: pandas dataframe with columns 'DATE', 'SALES', 'QUANTITY', 'PROMOS'

    Return:
        - df: baseline results in a pandas dataframe format with columns: 'dates', 'sales', 'quantity', 'promo',
                                                                          'baseline', 'baseline_quantity'
    """
    def __init__(self, df=None, selected_week_nb=None, args=None):
        self.df = df
        self.selected_week_nb = selected_week_nb
        self.args = args
        self.result = None
        self.baselinedetection()

    # Baseline detection
    def baselinedetection(self):
        # Data pre-processing
        # Calculate yearly average price
        self.df = self.df[self.df['SALES'] != 0.0]
        if len(self.df) > 1:
            # Set promo flag
            self.df['PROMO_FLAG'] = self.df['PROMOS']

            # Set NA values for promo sales and fill NA by interpolating
            df_np = self.df.copy()
            df_np.loc[df_np.PROMO_FLAG > 0, "SALES"] = np.nan
            df_np['SALES'] = df_np['SALES'].interpolate(method='linear', limit_direction='both', axis=0)
            df_np.loc[df_np.PROMO_FLAG > 0, "QUANTITY"] = np.nan
            df_np['QUANTITY'] = df_np['QUANTITY'].interpolate(method='linear', limit_direction='both', axis=0)

            # ALS baseline
            baseline_als_values = baseline_als(np.asarray(df_np['SALES'].astype(float)),
                                               lam=self.args['als_lambda'],
                                               p=self.args['als_weighting'],
                                               niter=100)

            baseline_als_quantity_values = baseline_als(np.asarray(df_np['QUANTITY'].astype(float)),
                                                        lam=self.args['als_lambda'],
                                                        p=self.args['als_weighting'],
                                                        niter=100)

            # Result
            result = {}
            result['dates'] = np.asarray(self.df['DATE'])                       # dates
            result['sales'] = np.asarray(self.df['SALES'].astype(float))        # sales
            result['quantity'] = np.asarray(self.df['QUANTITY'].astype(float))  # quantity
            result['promo'] = self.df['PROMO_FLAG'].astype(float).values        # promo flag
            result['baseline'] = baseline_als_values                            # baseline
            result['baseline_quantity'] = baseline_als_quantity_values          # baseline quantity
        else:
            # Result
            result = {}
            result['dates'] = []                                                # dates (year-week)
            result['sales'] = []                                                # sales
            result['quantity'] = []                                             # quantity
            result['promo'] = []                                                # promo flag
            result['baseline'] = []                                             # baseline
            result['baseline_quantity'] = []                                    # baseline quantity

        result = pd.DataFrame.from_dict(result)
        self.result = result

        return
