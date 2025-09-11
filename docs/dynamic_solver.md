# Dynamic Solver

PyFiberAmp's dynamic solver advances optical powers $P_k(z,t)$ and the excited-state population $N_2(z,t)$ along the fiber by numerically integrating the coupled rate equations.

For each optical channel $k$ with small-signal absorption $\alpha_k = \sigma_{a,k} \Gamma_k N_t$, small-signal gain $g_k^* = \sigma_{e,k} \Gamma_k N_t$, linear loss $\ell_k$, frequency $\nu_k$ and spectral width $\Delta\nu_k$, the solver propagates

\[
\frac{\partial N_2}{\partial t} = \sum_k \frac{\sigma_{a,k} P_k}{h\nu_k A_k} - \sum_k \frac{\sigma_{a,k} + \sigma_{e,k}}{h\nu_k A_k} P_k \frac{N_2}{N_t} - \frac{N_2}{\tau},
\]
\[
\frac{\partial P_k}{\partial z} = \Big[ \sigma_{e,k} N_2 - \sigma_{a,k}(N_t-N_2) - \ell_k \Big] P_k + m\, h\nu_k \Delta\nu_k \sigma_{e,k} N_2,
\]
where $h$ is Planck's constant, $A_k$ is the effective doped area, $m$ is the number of ASE polarization modes and $\tau$ is the upper-state lifetime.

Input powers and reflections are applied through `DynamicBoundaryConditions`, and the solver alternates between propagation along $z$ and population evolution in time using a backward–forward error compensation and correction (BFECC) scheme. Convergence is monitored from the change in $N_2$ and the iteration stops when a steady state is reached within the user-defined tolerance or after the requested number of time steps.

