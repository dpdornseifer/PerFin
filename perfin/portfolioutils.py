""" Contains utils to work with portfolios. These utils are also directly attached to the portfolio class. """
import cvxopt as opt
import numpy as np
from cvxopt import blas, solvers


def get_returns(prices):
    """ Returns the returns for the given stocks over the given timespan.


    Args:


    Returns:

    """
    # TODO return log returns to get rid of autocorrlation
    return prices.pct_change().dropna()


def markowitz_optimizer(returns):
    """ Does a markowitz distribution optimization for the stocks in the given portfolio.

    Returns:
        The optimal weight distribution of stocks in the portfolio by following the 'MPT' a.k.a/
        modern portfolio theory. It should help users to rebalance a given portfolio.


    Notes:
        This method is based on code listed in the following blog post:
        https://plot.ly/ipython-notebooks/markowitz-portfolio-optimization/

    """
    # TODO print current weight distribution vs. optimal distribution
    # TODO show the current return / sharpe .... vs. the optimal one
    # TODO performance optimization

    n = len(returns)
    returns = np.asmatrix(returns)

    N = 100
    mus = [10 ** (5.0 * t / N - 1.0) for t in range(N)]

    # Convert to cvxopt matrices
    S = opt.matrix(np.cov(returns))
    pbar = opt.matrix(np.mean(returns, axis=1))

    # Create constraint matrices
    G = -opt.matrix(np.eye(n))  # negative n x n identity matrix
    h = opt.matrix(0.0, (n, 1))
    A = opt.matrix(1.0, (1, n))
    b = opt.matrix(1.0)

    # Calculate efficient frontier weights using quadratic programming
    portfolios = [solvers.qp(mu * S, -pbar, G, h, A, b)['x']
                  for mu in mus]
    ## CALCULATE RISKS AND RETURNS FOR FRONTIER
    returns = [blas.dot(pbar, x) for x in portfolios]
    risks = [np.sqrt(blas.dot(x, S * x)) for x in portfolios]
    ## CALCULATE THE 2ND DEGREE POLYNOMIAL OF THE FRONTIER CURVE
    m1 = np.polyfit(returns, risks, 2)
    x1 = np.sqrt(m1[2] / m1[0])
    # CALCULATE THE OPTIMAL PORTFOLIO
    wt = solvers.qp(opt.matrix(x1 * S), -pbar, G, h, A, b)['x']
    return np.asarray(wt), returns, risks


def get_correlations():
    """ Returns the covariance matrix to give the user an idea how returns of certain stocks are correlated
        to each other.
    """
    pass


def get_stats():
    """ Returns the portfolio stats over the given timespan. """
    # sharpe
    # return
    # classical backtesting
    pass


def get_investment_recommendation():
    """ Returns the weight differences between the current distribution and the optimal distribution.
        The focus is just on stocks which are already in the portfolio.
    """
    pass