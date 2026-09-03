# Regional CO2 Storage Potential as a System-Scale Poromechanical Property

This directory contains the input files used for the conceptual one-cell
examples presented in the paper

    "Regional CO2 Storage Potential as a System-Scale Poromechanical Property"

by Tor Harald Sandve, Svenn Tveit, and Sarah Gasda.

The purpose of these examples is to illustrate how mechanical
confinement influences pressure-limited storage capacity. The model
consists of a single active grid cell representing a homogeneous
storage compartment. By eliminating geological heterogeneity and
pressure gradients, the response can be interpreted directly in terms
of the analytical expressions developed in the paper.

The examples include:

- ONECELL_TEST.DATA
  Simulation based solely on fluid and rock compressibility.

- ONECELL_TEST_TPSA.DATA
  Fully coupled flow-geomechanical simulation using the TPSA
  (Two-Point Stress Approximation) formulation.

## Running the examples

Simulation based on fluid and rock compressibility:

    flow ONECELL_TEST.DATA \
        --solver-max-time-step-in-days=366

Coupled flow-geomechanical simulation:

    flow ONECELL_TEST_TPSA.DATA \
        --tpsa-linear-solver=tpsa_linear_solver_hypre.json \
        --solver-max-time-step-in-days=366


## The Troll Aquifer model
For the Troll aquifer model, contact the Norwegian Offshore Directorate https://www.sodir.no/en/


## Software availability

The TPSA implementation used in this study is included in the OPM Flow
simulator from release 2026.10 and later.

OPM Flow:
https://opm-project.org

## Reference

If you use these examples, please cite:

Sandve, T.H., Tveit, S., and Gasda, S.,
"Regional CO2 Storage Potential as a System-Scale Poromechanical Property",
submitted to the International Journal of Greenhouse Gas Control.