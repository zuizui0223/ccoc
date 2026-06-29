# Island flower-colour empirical scenario template

This folder is a **pre-analysis scaffold**, not an empirical result.  It is
intended for an island flower-colour project in which several processes could
produce similar geographic colour differences.

## Focal question

A suitable question is not simply “what causes white flowers?”  It is:

> Across a predeclared family of ecological programs and robustness cells, which
> mechanisms remain necessary to explain the observed flower-colour, pollination,
> common-garden, and population-genetic signatures?

## Candidate motif vocabulary

Start with a deliberately revisable vocabulary such as:

- `pollinator_selection`: colour-dependent visitation, pollen transfer, or
  fitness makes a colour state selectively favoured;
- `founder_drift`: colonisation and small effective size create a colour shift
  without colour-specific selection;
- `plastic_response`: colour changes with environment or developmental context;
- `linked_trait_selection`: colour covaries with another selected trait; and
- `gene_flow_constraint`: restricted migration maintains an existing difference.

These are not mutually exclusive by default.  A candidate program must state
which motifs are active and which biological compatibility constraints are
assumed.

## Data contract

The file [`data_dictionary.csv`](data_dictionary.csv) defines the minimum raw
records.  Keep raw observations separate from derived binary traits.  For
example, a “no pollinator association” result must retain its observation time,
flower count, taxonomic resolution, detection model, and uncertainty rather
than being entered directly as a hard NULL.

## Before analysing the data

1. Fill in the motif definitions and trait-rule justification in a dated
   analysis plan.
2. Specify which outcomes are hard observations.  Most field non-detections
   should use `TraitDetection` with empirically justified sensitivity instead.
3. Define candidate programs before seeing the decisive response variables.
4. Mark program-universe coverage as `sampled` unless an enumeration or solver
   has shown it is complete.
5. Specify required robustness cells, such as alternative visit-classification
   rules, neutral-marker filters, seasonal subsets, or observation-channel
   calibrations.
6. Use the panel optimizer to identify the next most useful field, genetic, or
   common-garden observation; do not interpret the template as evidence.

## What counts as a real validation

A publishable empirical validation should include all of the following:

- raw field, pollinator, genetic, and common-garden data with site and sampling
  metadata;
- an independently justified observation/detection model;
- predeclared competing program families, including plausible non-focal routes;
- a robustness analysis over the stated cells;
- a record of which candidate programs were evaluated and whether the universe
  is sampled or complete; and
- a comparison between the panel recommended before data collection and the
  information actually obtained after data collection.

The immediate next step is to populate the data contract from the island field
project and write the candidate-program map with domain experts.  Until then,
no motif should be presented as empirically invariant.
