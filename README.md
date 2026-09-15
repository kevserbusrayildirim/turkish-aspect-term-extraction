# Turkish Aspect Term Extraction: Dataset & BERT-ELECTRA Fusion Model

This repository provides (1) a 6,000-instance Turkish Aspect-Based Sentiment Analysis (ABSA) dataset for aspect term extraction (ATE) research, spanning multiple domains (products, accommodation, education, social media, and more), and (2) the training/evaluation code for our proposed dual-encoder (BERT+ELECTRA) BiLSTM-CRF architecture. 

## Contents

| File | Rows | Description |
|---|---|---|
| `6k_absa_train.csv` | 4,500 | Training split |
| `6k_absa_dev.csv` | 750 | Validation split |
| `6k_absa_test.csv` | 750 | Held-out test split |
| `fusion_model.ipynb` | — | Training/evaluation notebook for the proposed architecture |

Each row contains:

| Column | Description |
|---|---|
| `text` | Original sentence |
| `target` | List of aspect term(s) mentioned in the text, exactly as they appear (inflected/compound forms preserved) |
| `polarity` | List of sentiment polarities (`positive` / `negative` / `neutral`), aligned by position with `target` |
| `category` | Domain/category label (e.g. `product`, `accommodation`, `education`, `social_media`) |
| `tokens` | Word-level tokenization of `text` |
| `labels` | BIOS tag sequence aligned to `tokens` (`B`/`I`/`O`/`S`) |
| `category_cleaned` | Normalized category label used for downstream grouping |
| `source` | Provenance of the instance — `collected` (gathered from online platforms) or `LLM-generated` (see below) |

## Tagging scheme

Aspect terms are labeled at the word level using the **BIOS** scheme: `B` (beginning of a multi-word aspect), `I` (inside), `O` (outside/non-aspect), `S` (single-word aspect). A sentence may contain zero, one, or multiple aspect terms, each with its own polarity.

## Annotation process

Text was collected from diverse online sources (e-commerce, accommodation/travel platforms, streaming/TV/film platforms, social media, and forums), excluding very short or semantically incomplete sentences, and excluding any personal information or offensive/discriminatory content. Aspect terms were annotated exactly as they appear in the source text.

**Inter-annotator agreement.** To assess annotation reliability, an independent study was conducted on a random 50-instance sample: two annotators, blind to the original labels and to each other's responses, independently re-labeled aspect terms and polarity for the same sentences, following the same annotation guidelines used in the original collection. Agreement was measured at the word level (each annotator's aspect spans converted to BIOS tags) via Cohen's κ, span-level exact-match F1 (seqeval), and Cohen's κ on polarity for jointly-identified aspects.

| Comparison | Token κ (BIOS) | Span-F1 | Polarity κ |
|---|---|---|---|
| Annotator 1 vs. Annotator 2 | 0.62 | 0.64 | 0.69 |
| Annotator 1 vs. original labels | 0.58 | 0.62 | 0.65 |
| Annotator 2 vs. original labels | 0.70 | 0.73 | 0.86 |

Residual disagreement is concentrated almost entirely in span-boundary choice (e.g., whether a preceding possessive/modifier is included in the aspect span) rather than in aspect presence or polarity — both annotators agree once an aspect span is settled.

## Data quality audit and split strategy

A full audit of the train/validation/test split was conducted to verify strict isolation between the data used for hyperparameter selection and the data used for final evaluation. The audit identified 10 problematic instances among the original 6,000 (0.17%): 8 exact duplicates spanning split boundaries and 2 instances with inconsistent annotation across collection passes. These were corrected — the 2 ambiguous instances were replaced with new, unambiguous examples — and the full 6,000-instance pool was re-partitioned into a fixed 4,500/750/750 train/validation/test split using a single random seed, with **zero text-level overlap** between any two splits (verified programmatically).

Ten instances in the pool are `LLM-generated` rather than `collected`, added during this audit to restore the dataset to exactly 6,000 instances after removing the 8 exact duplicates and 2 ambiguous instances; they follow the same BIOS annotation convention and are explicitly flagged via the `source` column for transparency.

## Reproducing the experiments

The training/evaluation code for the proposed architecture (BERT+ELECTRA dual-encoder BiLSTM-CRF with convex-combination fusion, BIOS scheme, duplicate subword propagation) is provided as a Colab notebook: [`fusion_model.ipynb`](fusion_model.ipynb). See the notebook's first cell for setup instructions (Google Drive mount, GPU runtime).

## License and citation

This dataset is intended for academic and research purposes only. Any use of the dataset in publications or projects must include a proper citation of the original source.

Bu veri kümesi yalnızca akademik ve araştırma amaçlı kullanılabilir. Veri kümesini kullandığınız tüm çalışmalar ve yayınlarda kaynak belirtilmesi zorunludur.

*(Citation details will be added upon publication.)*
