# Annotation Guidelines

These guidelines describe how aspect terms and their sentiment polarity were annotated for this dataset, and how they should be annotated if the dataset is extended or independently re-annotated (e.g., for inter-annotator agreement checks).

## Task

For each sentence, identify every **aspect term** — a word or short phrase naming a specific product, service, or experience feature that the writer expresses an opinion about — and assign each one a **polarity**: `positive`, `negative`, or `neutral`.

A sentence may contain zero, one, or multiple aspect terms, each independently polarized.

## How to mark an aspect term

1. **Copy the text exactly as it appears in the sentence**, including its inflected or compound form. Do not lemmatize or normalize (e.g., if the sentence says `"telefonu"`, write `"telefonu"`, not `"telefon"`). This is required for the automatic BIOS-tag alignment (see `annotation_helper.py`) to locate the span correctly.
2. Keep the span as **short as possible while still naming the feature**. Prefer the bare noun/noun phrase over a longer phrase that also includes a possessive, article, or evaluative modifier.
   - Prefer `"temizlik"` over `"Otelin genel temizliği"`.
   - Prefer `"konumu"` over `"Mekanın konumu"`.
   - The evaluative part of the sentence (`"çok iyiydi"`, `"berbattı"`) determines the *polarity*, not the span — it should not be included in the aspect term itself.
3. If a sentence expresses the same opinion about a feature using two or more nearby words, treat it as **one multi-word aspect term** only if the words form a single coherent noun phrase naming one feature (e.g., `"şarj süresi"`, `"kahvaltı menüsü"`). Do not merge two separate features into one span (e.g., in *"oda ve banyo çok temizdi"*, `"oda"` and `"banyo"` are two separate aspect terms, not one).
4. If the same feature is mentioned by more than one surface form in the same sentence, annotate each mention as its own aspect term instance, at its own position.

## How to assign polarity

- `positive` / `negative`: the sentence contains **explicit evaluative language** about the feature (e.g., `"harika"`, `"çok kötü"`, `"berbat"`, `"gayet iyi"`, `"yetersizdi"`).
- `neutral`: the feature is mentioned but the sentence does not clearly evaluate it (purely descriptive/factual mention), **or** the evaluative language is genuinely ambiguous/mixed.
- Do not infer polarity from world knowledge or general association (e.g., mentioning a friend or a pleasant-sounding activity is not automatically `positive` — only mark polarity when the sentence itself expresses an evaluation).

## When there is no aspect term

Not every sentence in the source corpus contains an evaluable aspect term. If a sentence is **purely descriptive or narrative** — it states a fact or tells a story without evaluating a product/service feature — **do not force an aspect term**. Leave the aspect field empty. This is a valid, expected annotation outcome, not an error.

*Example (no aspect term):* `"bugün ingiliz kız arkadaşım ile kaykay sürüyoruz Sri Lankada yaşadığımız köyde bizim gibi bir çok yabancı yaşıyor."` — this is a personal narrative with no explicit evaluation of any feature; it should not be forced into an aspect-term annotation.

During this dataset's construction, exactly this situation caused two instances to be flagged as ambiguous during inter-annotator agreement testing; they were subsequently replaced with unambiguous examples containing explicit, contrastive aspect+polarity pairs (see the main [README](README.md), "Data quality audit and split strategy").

## Sentence exclusion criteria (applied during collection, before annotation)

Do not include a candidate sentence in the dataset if it is:
- Very short or semantically incomplete (fragments, single words).
- Lacking any potential aspect term altogether (pure greetings, pure exclamations).
- Shorter than roughly one-third the combined length of its own aspect terms (a heuristic against near-empty/low-information sentences).
- Containing personal information (names of private individuals, contact details, addresses) or content that is offensive, discriminatory, or could constitute a criminal offense.

## Worked examples

| Text | Aspect Terms | Polarity |
|---|---|---|
| `"Kargo çok hızlı geldi ama kutu hasar görmüştü."` | `"Kargo"`, `"kutu"` | `positive`, `negative` |
| `"Yaşadığımız köydeki kaykay parkı harika ama gece aydınlatması çok yetersizdi."` | `"kaykay parkı"`, `"gece aydınlatması"` | `positive`, `negative` |
| `"Otelin genel temizliği çok iyiydi."` | `"temizlik"` (not `"Otelin genel temizliği"`) | `positive` |
| `"Bugün hava çok güzeldi, parkta yürüyüş yaptık."` | *(none — no evaluable feature)* | — |

## Blind re-annotation protocol (for inter-annotator agreement)

When re-annotating a sample for IAA measurement:
1. Annotators must work **independently**, without seeing the original/gold labels or each other's answers.
2. Provide only the raw `text` column — never the original `target`/`polarity`/`labels` columns.
3. Follow the span and polarity rules above exactly as written; when in doubt, prefer the shorter span (see "How to mark an aspect term," rule 2) and `neutral` polarity over a forced strong polarity.
4. Agreement is computed at the word level: aspect spans are converted to BIOS tags via automatic substring matching against the sentence tokens (see `annotation_helper.py`), then compared via Cohen's κ and span-level F1 (seqeval). Polarity agreement (Cohen's κ) is computed only over aspects both annotators identified.
