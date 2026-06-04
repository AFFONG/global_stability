from sympy import Matrix, symbols, sqrt, simplify, lambdify
import numpy as np

def _build():
    Ui = Matrix(list(symbols("ui0:5")))
    Uj = Matrix(list(symbols("uj0:5")))
    
    # CHANGED: Replaced Ax, Ay, Az with unit normal components nx, ny, nz.
    # Area magnitude 'A' is completely omitted from the calculations.
    nx, ny, nz = symbols("nx ny nz")
    nij = Matrix([nx, ny, nz])
    
    Vi, g = symbols("V_i gamma")

    def dot(a, b):
        return (a.T @ b)[0, 0]

    rhoi = Ui[0]; ui = Ui[1:4, :] / rhoi
    rhoj = Uj[0]; uj = Uj[1:4, :] / rhoj
    pi = (Ui[4] - rhoi * dot(ui, ui) / 2) * (g - 1)
    pj = (Uj[4] - rhoj * dot(uj, uj) / 2) * (g - 1)


    # CHANGED: All flux contributions now project onto the unit normal vector (nij)
    C = dot(rhoi * ui + rhoj * uj, nij) / 2
    M = (rhoi * ui * ui.T + rhoj * uj * uj.T) @ nij / 2
    G = (pi + pj) / 2 * nij
    # Ui[4] = rho * E
    K = dot(((Ui[4] + pi) * ui + (Uj[4] + pj) * uj) / 2, nij)

    Ri = Matrix([[C], M + G, [K]])

    print("[inviscid_central] Building symbolic Jacobian...")
    J_sym = simplify(Ri.jacobian(Matrix([*Ui, *Uj])))
    
    # CHANGED: Updated the symbolic arguments tuple to accept nx, ny, nz, g
    sym_args = (*Ui, *Uj, nx, ny, nz, g)
    fn_i = lambdify(sym_args, J_sym[:, :5], modules="numpy")
    fn_j = lambdify(sym_args, J_sym[:, 5:], modules="numpy")

    # CHANGED: Updated function signature to accept nx_val, ny_val, nz_val instead of Aij_val
    def jacobian_fn(Ui_val, Uj_val, nx_val, ny_val, nz_val, gamma_val):
        a = (
            *np.asarray(Ui_val, float), 
            *np.asarray(Uj_val, float), 
            float(nx_val), 
            float(ny_val), 
            float(nz_val), 
            float(gamma_val)
        )
        return np.array(fn_i(*a), dtype=float), np.array(fn_j(*a), dtype=float)

    return jacobian_fn

compute_central_jacobian = _build()