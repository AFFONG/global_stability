from sympy import Matrix, symbols, sqrt, simplify, lambdify
import numpy as np

def _build():
    Ui  = Matrix(list(symbols("ui0:5")))
    Uj  = Matrix(list(symbols("uj0:5")))
    Ax, Ay, Az = symbols("Ax Ay Az")
    Aij = Matrix([Ax, Ay, Az])
    Vi, g = symbols("V_i gamma")

    def dot(a, b):
        return (a.T @ b)[0, 0]

    rhoi = Ui[0];  ui = Ui[1:4, :] / rhoi
    rhoj = Uj[0];  uj = Uj[1:4, :] / rhoj

    pi = (Ui[4] - rhoi * dot(ui, ui) / 2) * (g - 1)
    pj = (Uj[4] - rhoj * dot(uj, uj) / 2) * (g - 1)

    R       = sqrt(rhoj / rhoi)
    rho_roe = sqrt(rhoi * rhoj)
    u_roe   = (ui + R * uj) / (1 + R)
    Hi      = (Ui[4] + pi) / rhoi
    Hj      = (Uj[4] + pj) / rhoj
    H_roe   = (Hi + R * Hj) / (1 + R)
    p_roe   = (g - 1) / g * rho_roe * (H_roe - dot(u_roe, u_roe) / 2)

    C  = dot(rho_roe * u_roe, Aij)
    M  = (rho_roe * u_roe * u_roe.T).T @ Aij
    G  = p_roe * Aij
    K  = dot(rho_roe * H_roe * u_roe, Aij)
    Ri = -Matrix([[C], Matrix(M) + G, [K]]) / Vi

    print("[inviscid_roe] Building symbolic Jacobian...")
    J_sym = simplify(Ri.jacobian(Matrix([*Ui, *Uj])))

    sym_args = (*Ui, *Uj, Ax, Ay, Az, Vi, g)
    fn_i = lambdify(sym_args, J_sym[:, :5], modules="numpy")
    fn_j = lambdify(sym_args, J_sym[:, 5:], modules="numpy")

    def jacobian_fn(Ui_val, Uj_val, Aij_val, Vi_val, gamma_val):
        a = (*np.asarray(Ui_val, float), *np.asarray(Uj_val, float),
             *np.asarray(Aij_val, float), float(Vi_val), float(gamma_val))
        return np.array(fn_i(*a), dtype=float), np.array(fn_j(*a), dtype=float)

    return jacobian_fn

# Built once on import
compute_roe_jacobian = _build()