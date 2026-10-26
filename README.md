# Terpene exposure transcriptomics: reproducibility and context

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Terpedia/research-transcriptomics/blob/main/notebooks/terpene_exposure_pilot.ipynb)

Open the notebook in Colab and run all cells. This repository is private during development: Colab may request GitHub authorization to open the notebook; its setup cell separately requests a read-access token to clone the supporting files. Credentials are entered invisibly and are not written to the notebook or Git remote.


## Research question

**Which metabolic and signaling responses to terpene exposure are reproducible, and which depend on cellular context or a specific target?**

This project will combine transcriptomic perturbation data for defined terpene/terpenoid exposures with genetic perturbation data (including Perturb-seq) relevant to experimentally nominated targets and pathways. The initial publicly retrievable studies are dominated by microbial antifungal/antibacterial exposure models; they should not be generalized to mammalian cells or human effects.

## Why this question / computational biology portfolio framing

This is a case study in perturbation biology: estimate treatment effects with replication, distinguish biological response from dose/time and technical context, represent uncertainty at gene and pathway levels, and connect chemical perturbations to genetic perturbations without overstating causality. It foregrounds skills central to single-cell functional genomics work: design-aware statistics, perturbation-effect estimation, QC, context-stratified analysis, reproducible pipelines, model-ready data, and clear collaboration between computational and experimental work.

The current treatment datasets are bulk microbial RNA-seq, so they are a methods sandbox and a bounded biological example, not a proxy for human variant-level Perturb-seq. A stronger next extension is to add a public Perturb-seq dataset with raw/processed cells and perturbation labels, then demonstrate guide/perturbation QC, pseudobulk or donor-aware effects, cell-state stratification, and uncertainty. For a job application, describe what is implemented and what remains planned distinctly.

## Current discovery snapshot

The candidate inventory is in [`datasets.json`](datasets.json). The highest-priority RNA-seq records are:

1. **Terpinen-4-ol and 1,8-cineole, *Botrytis cinerea*** — GSE138291 / PRJNA575349, with terpinen-4-ol and 1,8-cineole arms and triplicate sequencing. The paper describes terpinen-4-ol-associated metabolism, amino-acid/carbohydrate/lipid responses, cell integrity and mitochondrial function, while 1,8-cineole affected genetic-information-processing functions. Treat the mixed tea-tree-oil arm separately from pure-compound arms.
2. **Limonene, *Penicillium digitatum* DSM 62840** — RNA-seq with limonene at 840 mg/L for 12 h, two biological replicates, a time-matched untreated control and a 0 h reference. Reported candidate responses include secondary metabolism, energy metabolism, TCA/oxidative phosphorylation, ABC transporters, and limonene biotransformation. The low replicate count and high exposure concentration make this a discovery dataset, not a robust general-response estimate.
3. **Linalool, *Listeria monocytogenes* ATCC 19115** — GSE136998 records an 8 h, 1× MIC contrast (0.5% v/v; 4.35 mg/mL), with an untreated control and qRT-PCR follow-up in the paper. Although the methods describe 4, 8 and 12 h sampling, GEO's series-level design only confirms the 8 h contrast; sample-level replication and availability of other timepoints need verification. Strong antimicrobial exposure may capture terminal stress/cell damage as well as mechanism; model time and viability explicitly.

The selected analysis set is documented in [`manuscript/selected-datasets.md`](manuscript/selected-datasets.md): GSE138291 (*B. cinerea*, 15 samples), PRJNA913446 (linalool in *F. oxysporum*, six samples), and PRJNA608617 (R-(+)-limonene in *P. digitatum*, six samples). Their sample-level accessions and treatment assignments are frozen in [`data/selected_studies/sample_manifest.tsv`](data/selected_studies/sample_manifest.tsv). GSE138291's processed matrix has been analyzed descriptively in the [executed Terputer notebook](https://github.com/Terpedia/terpedia-transcriptomics-demo/blob/2681004/notebooks/terputer-transcriptomics.ipynb); the other two cohorts remain metadata-only. A separate 30/120-minute linalool exposure study in *B. cinerea* remains in reserve pending accession and raw-data verification.

The exact-chemical ingestion must exclude essential-oil mixtures from pure-compound analyses, retain stereochemistry where reported, and distinguish treatment exposure from endogenous terpene biosynthesis, infection, or chemotype comparisons.

### Reproducible pilot artifact

[`scripts/analyze_gse136998.py`](scripts/analyze_gse136998.py) downloads GEO's processed GSE136998 RSEM FPKM matrix and writes a descriptive per-gene treatment/control summary plus a source checksum and run manifest under [`results/gse136998/`](results/gse136998/). Run from this repository with `python scripts/analyze_gse136998.py` (or from the project root with `python scripts/analyze_gse136998.py`). This is intentionally not a differential-expression test: the available matrix is FPKM, so the output has no p-values and should be treated as an exploratory ranking only. It currently uses GEO's opaque `geneN` identifiers; a versioned annotation crosswalk is a required next step.

The notebook [`notebooks/terpene_exposure_pilot.ipynb`](notebooks/terpene_exposure_pilot.ipynb) captures the research question, study design, provenance/checksum verification, methods, saved descriptive tables, plotting code, results, interpretation and limitations. It reads the checked-in source matrix and run manifest. To rerun every cell interactively, use a Python 3 Jupyter environment with pandas, NumPy and Matplotlib installed. Saved result tables are embedded in the notebook so they can be reviewed without rerunning it.

## Hypotheses to test

- **Candidate shared cellular stress/metabolism programs:** membrane/cell-envelope integrity, transport/efflux, redox/oxidative stress, energy metabolism, and translation/ribosome response may recur across terpene exposures, but may reflect nonspecific growth inhibition at high or lethal doses.
- **Compound-specific responses:** terpinen-4-ol, 1,8-cineole, linalool and limonene should remain distinct treatments. Similar labels such as “metabolism” are not enough; compare directionally consistent ortholog-level genes and pathway modules.
- **Context dependence:** species, strain, cell type, medium, dose, exposure route, time and baseline viability may explain apparent disagreement. Plant host response and microbial direct-exposure response are separate evidence strata.
- **Target dependence:** use Perturb-seq/CRISPR perturbations only to test target/pathway dependency after a direct target claim has been supported by independent binding, biochemical, genetic-rescue or pharmacological evidence. A matching knockdown signature alone does not establish binding or mediation.

## Analysis plan

1. Freeze a source registry: accession, article/DOI/PMID, organism and strain, exact compound identifier (ChEBI/PubChem/InChIKey and stereochemistry), formulation/vehicle, concentration, time, exposure route, controls, biological replicate, library/read layout, reference genome/annotation release, assay, and license/reuse constraints.
2. Prefer author-supplied raw reads and processed count/DE tables; retain checksums and retrieval dates. Reprocess raw reads with a documented organism-appropriate pipeline when feasible. Do not combine published DEG lists with incompatible thresholds as if they were a common effect-size matrix.
3. Estimate within-study treatment effects and uncertainty from counts using a consistent model. Include dose/time contrasts and matched vehicle/time controls; record viability/growth inhibition and exclude or flag terminally toxic conditions in sensitivity analyses.
4. Map genes to stable species-specific identifiers and orthogroups. Do not equate genes by symbol alone. Analyze pathway/module effects within species first; cross-species synthesis uses one-to-one/high-confidence orthology and direction-preserving rank statistics.
5. Estimate reproducibility at three levels: exact compound across studies; chemical class only as exploratory; and shared stress/metabolic modules across different compounds. Report heterogeneity and prediction intervals where there are enough independent studies; otherwise report a descriptive replication matrix.
6. Integrate Perturb-seq or CRISPR signatures as **genetic perturbation evidence**, not terpene-exposure observations. Compare signatures conditional on same cell model and time where possible. Test target-dependence using interaction/epistasis evidence when datasets permit.
7. Store gene/pathway claims at their smallest evidence-bearing unit and label them observed expression, orthology-supported recurrence, genetic dependency, target-validated, or hypothesis. Expression change alone does not demonstrate enzyme activity, metabolite flux, receptor engagement, or pathway causality.

## Statistical principles to carry into a single-cell extension

- Treat the biological replicate (donor, culture, or independently prepared sample) as the unit for inference; cells are subsamples, not independent replicates.
- Use pseudobulk by biological replicate × perturbation × cell type/state or a validated mixed model with donor/batch structure. Keep guide-level effects available and aggregate only after guide QC.
- Estimate perturbation efficiency and assignment uncertainty; retain non-targeting controls and, where relevant, safe-targeting controls. Check multiple guides and negative-control distributions.
- Separate cell abundance/composition changes from within-state expression changes. Model cell-state shifts as outcomes, not merely covariates to regress away.
- Pre-specify contrasts and minimum replication/QC gates. Include donor, batch, library, and perturbation interactions when supported by design; avoid fitting non-identifiable covariates.
- Produce model-ready effect records with stable feature IDs, log fold changes, uncertainty, sample/cell context, perturbation identity, covariates, QC flags, and a frozen train/validation/test split grouped by donor or experiment to prevent leakage.

## Terpedia ingestion design

Keep large FASTQ files and bulky matrices in their source repositories/object storage; the Terpedia repository should hold stable provenance, metadata, analysis outputs and compact evidence records. Proposed layers:

- `sources`: publication, GEO/BioProject/SRA or other accession, landing URL, license, retrieved timestamp, checksum, processing version.
- `experiments`: organism/taxon, strain/cell model, treatment design, control, replicate, dose/unit, duration, vehicle, exposure route, viability and assay details.
- `compounds`: exact chemical entity and identifiers; mixtures are explicit mixture entities with composition evidence and never silently expanded into single-compound treatments.
- `expression_effects`: gene/transcript identifier, genome/annotation version, contrast, log2 fold change, standard error/statistic, p-value and adjusted p-value, count/normalization provenance.
- `pathway_evidence`: pathway identifier/version, tested gene universe, enrichment statistic and correction, contributing genes, direction consistency, evidence class and source experiment.
- `cross_context_summaries`: orthology mapping, contexts included, model/heterogeneity estimates, reproducibility rule, exclusions and caveats.
- `genetic_perturbations`: target gene, perturbation type/guide, cell context, effect estimate and assay. These records remain distinguishable from compound-treatment records.

Use explicit RDF/SQL mappings only after inspecting the destination Terpedia schema and load mechanism. Do not directly publish into a live graph from this exploratory package. Initial deliverable is a validated manifest and reproducible analysis specification; ingestion can then target the selected graph/schema with source links intact.

## Decision gates before bulk ingestion

- Confirm each accession maps to the claimed compound arm and obtain sample-level treatment metadata.
- Confirm licensing and raw/processed file availability; record file checksums.
- Harmonize exact chemical identity, concentration units, vehicle, and condition labels.
- Verify at least two biological replicates per contrast, flagging exceptions rather than silently pooling.
- Establish organism-specific gene annotation and crosswalk versions.
- Select the target Terpedia table/graph, URI policy and ingestion interface.

## References and data discovery

- Gao et al. 2019, linalool vs. *L. monocytogenes*, GSE136998: https://doi.org/10.3389/fmicb.2019.02947
- Zhang et al. 2020, limonene biotransformation in *P. digitatum*: https://doi.org/10.3389/fmicb.2020.00744
- *B. cinerea* response to tea-tree oil components, GSE138291 / PRJNA575349: https://www.ncbi.nlm.nih.gov/bioproject/575349
- Linalool antifungal response in *B. cinerea*, RNA-seq/proteome: https://doi.org/10.1021/acs.jafc.9b03103
- Terpene transcriptome screening should use Perturb-Seq resources for the genetic-context layer, e.g. PerturbSeqr data catalog: https://perturbseqr.maayanlab.cloud/download. These catalogs are discovery/processed-signature sources, not raw-data substitutes.

## Status

Literature/data discovery, two processed-FPKM exposure analyses, a processed Perturb-seq context comparison, and a 27-sample selection manifest are available. Raw reads have not been downloaded, and no cross-study reproducibility claim is yet established. Next step is to freeze raw file checksums and perform count-based analysis of the selected contrasts.

## White paper

The working manuscript is [Resolving reproducible and context-dependent responses to terpene exposure](manuscript/white-paper.md). Its [critical review](manuscript/critical-review.md) records the author-side audit and remaining release work. Executed results and proposed analyses are distinguished throughout.

The executed [signaling-context notebook](notebooks/signaling_context_comparison.ipynb) compares processed Perturb-seq effects for two A549 contexts using revision-pinned Arc Institute data. It demonstrates descriptive context comparison; raw-cell QC and replicated DE remain future work.


## Standalone study package

This directory is the local Terputer package for the terpene exposure transcriptomics study. It contains the source matrices and manifests needed by the included notebooks; no local virtual environment is included. From this directory, create the environment with `python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt`, then launch `jupyter lab notebooks/terpene_exposure_pilot.ipynb`. The executed notebook provides the GSE136998 descriptive pilot. `signaling_context_comparison.ipynb` is a separate processed genetic Perturb-seq context illustration. Neither supports a cross-study terpene replication claim.

File hashes and provenance are listed in [`data/manifest.tsv`](data/manifest.tsv).


## Terpedia access

The optional client in `src/terpedia_access.py` calls the Terpedia Knowledge API at `/v1/tabular/search`. It reads `TERPEDIA_KNOWLEDGE_API_KEY` and `TERPEDIA_KB_API_URL` from the process environment and sends the key in the `x-knowledge-key` header. Copy `.env.example` as a configuration reference, then provide the real key through a local secret manager, Codespaces secret, or authorized GitHub Actions secret. Never commit `.env` or print the key in notebook output.
