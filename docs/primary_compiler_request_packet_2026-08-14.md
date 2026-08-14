# Primary compiler source request packet — 2026-08-14

> **Purpose:** turn issue #122's remaining historical compiler gate into concrete acquisition actions. This packet does not add evidence for H1–H4. It only fixes request text, provenance fields, and the extraction checklist to use when primary construction pages arrive.

## Stop rule

Do **not** reopen broad web searching. The remaining problem is primary-text acquisition and reading. Failure to retrieve a source is not evidence that H1–H4 fail.

## A. Weiner & Hopcroft (1968), Technical Report no. 61

### Bibliographic target

- Peter Weiner; John E. Hopcroft
- *Bounded fan-in, bounded fan-out uniform decompositions of synchronous sequential machines*
- Princeton University, Digital Systems Laboratory, Technical Report no. 61
- April 1968
- extent: 7 pages + 3 leaves of plates
- University of Tokyo General Library: call no. `U600:769`, item `0004766739`, NCID `BA8670779X`

### Preferred direct request — Princeton Engineering Library

Current Princeton Library directory lists the Engineering Library contact as `englib@princeton.edu`.

**Subject**

`Digitization request — Digital Systems Laboratory Technical Report no. 61 (Weiner & Hopcroft, 1968)`

**Body**

> Dear Engineering Library staff,
>
> I am conducting historical research on modular synthesis of synchronous sequential machines and would like to ask whether a research scan or digitization can be supplied for the following Princeton Digital Systems Laboratory technical report:
>
> Peter Weiner and John E. Hopcroft, *Bounded fan-in, bounded fan-out uniform decompositions of synchronous sequential machines*, Technical Report no. 61, April 1968.
>
> Bibliographic records describe the item as 7 pages plus 3 leaves of plates. If digitization is possible, I would be grateful for the **complete report including all three plates**, subject to the Library's copyright and reproduction policies.
>
> The scan is needed to verify the construction details—module state/input/output resources, fan-in/fan-out bounds, source-input distribution, realization/output semantics, and timing/latency—not for redistribution.
>
> Please let me know whether the item can be digitized and whether any fee, request form, or other procedure is required.
>
> Thank you very much.

### Japanese fallback — University of Tokyo ILL

Tokyo University General Library's current guidance states that individual users cannot directly submit an ILL request; use an affiliated institution library or a public library. For NACSIS-ILL, the General Library participant ID is `FA001787`.

**Request text for the requesting library**

> 文献複写依頼を希望します。
>
> Peter Weiner; John E. Hopcroft, *Bounded fan-in, bounded fan-out uniform decompositions of synchronous sequential machines*, Princeton University Digital Systems Laboratory Technical Report no. 61, April 1968.
>
> 東京大学総合図書館所蔵：請求記号 `U600:769`、資料ID `0004766739`、NCID `BA8670779X`。
>
> 書誌上「7 p., [3] leaves of plates」となっているため、著作権・所蔵館規定の範囲内で、**本文7頁に加えて図版3葉を含む資料全体**の複写を希望します。
>
> 利用目的：同期順序機械の uniform modular decomposition に関する学術研究・先行研究確認。

## B. Newborn & Arnold (1972)

### Bibliographic target

- Monroe M. Newborn; Thomas F. Arnold
- *Universal Modules for Bounded Signal Fan-Out Synchronous Sequential Circuits*
- IEEE Transactions on Computers 21(1), January 1972, pp. 63–79
- DOI `10.1109/T-C.1972.223433`

### Osaka Prefectural Library Web Copy entry

The current Osaka Prefectural Library Web Copy service accepts online copy requests and can mail copies; the service is available to anyone, including one-time use without full user registration.

**Requested pages / note**

> IEEE Transactions on Computers, Vol. 21, No. 1 (January 1972), pp. 63–79.
>
> Monroe M. Newborn and Thomas F. Arnold, “Universal Modules for Bounded Signal Fan-Out Synchronous Sequential Circuits.”
>
> DOI: 10.1109/T-C.1972.223433.
>
> 調査研究目的。論文全体の複写を希望します（著作権法・所蔵館規定の範囲内）。

**Admission warning:** verify title, authors, volume/issue, and pages on receipt. Do not identify the paper from DOI alone; adjacent DOI confusion has already occurred in the audit.

## C. Drilman & Weiner (1972)

### Bibliographic target

- J. Drilman; Peter Weiner
- *Modular Networks and Nondeterministic Sequential Machines*
- IEEE Transactions on Computers 21(10), October 1972, pp. 1124–1129
- IEEE Xplore article number `1672054`

### Osaka Prefectural Library Web Copy entry

> IEEE Transactions on Computers, Vol. 21, No. 10 (October 1972), pp. 1124–1129.
>
> J. Drilman and Peter Weiner, “Modular Networks and Nondeterministic Sequential Machines.”
>
> 調査研究目的。論文全体の複写を希望します（著作権法・所蔵館規定の範囲内）。

**Do not add a DOI unless independently verified.** The current evidence ledger intentionally leaves it unset.

## D. Williams + Le Van–van Houtte (1975)

### Bibliographic targets

Same issue: IEEE Transactions on Computers 24(8), August 1975.

1. George H. Williams, *Uniform Decomposition of Incompletely Specified Sequential Machines*, pp. 840–843.
2. Tiu Le Van; Noël van Houtte, *Delayed Universal Logic Modules and Sequential Machine Synthesis*, pp. 853–855.

A Tokyo University of Technology library holding is already recorded in the acquisition ledger. The current public library site exposes an outside-user section and inquiry route, but this audit did not re-verify a specific postal-copy workflow. Therefore use an **inquiry**, not an assumed copy order.

**Inquiry text**

> 東京工科大学メディアセンター図書館 ご担当者様
>
> 調査研究目的で、貴館所蔵の *IEEE Transactions on Computers*, Vol. 24, No. 8 (August 1975) に掲載された以下2論文の利用・複写方法について確認したく、ご連絡いたしました。
>
> 1. George H. Williams, “Uniform Decomposition of Incompletely Specified Sequential Machines,” pp. 840–843.
> 2. Tiu Le Van and Noël van Houtte, “Delayed Universal Logic Modules and Sequential Machine Synthesis,” pp. 853–855.
>
> 学外者が調査研究目的で当該号を閲覧・複写する場合、来館利用、紹介状、事前申請、あるいは所属図書館経由の文献複写のいずれが利用可能かご教示いただけますでしょうか。
>
> 著作権法および貴館の利用規定に従って利用いたします。どうぞよろしくお願いいたします。

## E. On-receipt H1–H4 extraction form

For **every** recovered primary source, fill the following table from the construction text. Page/figure/theorem numbers are mandatory. If the source is silent, write `NOT ESTABLISHED`; do not infer.

| Clause | Exact extraction target | Evidence to record |
|---|---|---|
| H1 locality | local component state count; input/output arity; fan-in/fan-out or graph-degree bound; dependence on source state count and source input count | page/theorem/figure + literal construction statement |
| H2 controls | source input alphabet; encoding; external-input distribution/wiring; whether cost changes with source state count or restricted/open language | page/figure + explicit wiring/encoding rule |
| H3 trace faithfulness | formal realization/isomorphism definition; designated external outputs; whether internal signals are hidden; whether equivalence is two-way | definition/theorem + designated observable contract |
| H4 timing | source clock; module/network clock; delay/settling; source-step-to-output-valid latency; depth/diameter dependence | page/theorem + explicit timing formula/statement |
| fixed-hardware restriction | for incomplete/nondeterministic methods, whether different admissible specifications/refinements reuse one network or trigger resynthesis | exact construction/synthesis rule |

## F. Decision discipline

- **All H1–H4 verified with comparable overhead:** demote bounded-local/logarithmic-access existence as a firstness claim; keep the CCOC relay as explicit extremal/sharpness construction.
- **H1 but size-dependent H2/H4:** preserve a quantitative distinction for the fixed-control / degree-three / radius-one / logarithmic-access package.
- **Only one-way simulation:** H3 remains open; a compiler can create spurious closed-context distinctions.
- **Per-specification resynthesis:** treat as strong ancestry for contextual decomposition, not the same fixed-hardware grammar opening.

## G. Tracking

- parent historical gate: issue #122
- execution checklist: issue #185
- Ullman–Weiner construction-page blocker: issue #137
- canonical handoff: `docs/primary_source_request_handoff_2026-08-13.md`
- canonical evidence table: `docs/universal_compilation_source_audit.md`
