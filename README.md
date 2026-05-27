# global_stability_project

This repository contains a framework for performing **Global Stability Analysis**, focusing on the construction and assembly of linearized Jacobian matrices for CFD solvers.

## Project Structure

### `src/cfd_jacobian/`
Core modules for calculating the flux Jacobians:

* **`inviscid_central.py`** – Module to find the **Inviscid Jacobian** using **Central Averaging**.
* **`inviscid_roe.py`** – Module to find the **Inviscid Jacobian** using **Roe-averaging** 
* **`viscous.py`** – Module to find the **Viscous Jacobian** by spectural radius approximation

### `src/`
* **`main.ipynb`** – The **main branch** and primary entry point of the code. This notebook handles the global matrix assembly and eigenvalue solver execution.
