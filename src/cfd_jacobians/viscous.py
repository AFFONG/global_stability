import numpy as np

def compute_viscous_jacobian(mu, Pr, gamma, rho, xi, xj, mu_t=0.0, Pr_t=0.9):
    """
    Viscous flux Jacobian (spectral radius approximation).

    Parameters
    ----------
    mu    : float          dynamic viscosity
    Pr    : float          laminar Prandtl number
    gamma : float          specific heat ratio
    rho   : float          density at edge midpoint
    xi    : array (2,)|(3,) position of node i
    xj    : array (2,)|(3,) position of node j
    mu_t  : float          turbulent viscosity (default 0)
    Pr_t  : float          turbulent Prandtl number (default 0.9)

    Returns
    -------
    lambda_max : float
    J_G        : np.ndarray (n, n)  scalar * Identity
    """
    xi, xj = np.asarray(xi, dtype=float), np.asarray(xj, dtype=float)
    l_ij = np.linalg.norm(xj - xi)
    if l_ij == 0.0:
        raise ValueError("Nodes xi and xj are coincident (l_ij = 0).")

    max_term     = max(4.0 / (3.0 * rho), gamma / rho)
    prandtl_term = (mu / Pr) + (mu_t / Pr_t)
    lambda_max   = (1.0 / l_ij) * max_term * prandtl_term
    J_G          = lambda_max * np.eye(len(xi))

    return lambda_max, J_G