# Galaxy Viewer — Master Image Curation Memory

This directory is the authoritative memory of every image review performed for Galaxy Viewer.

## Purpose

A review decision is permanent history. Future curator pages MUST consult this directory before rendering candidates so the same image is not repeatedly shown.

## Decision contract

- `KEEP` — user wants the image. It is excluded from ordinary future candidate pages and retained for later routing into an observatory/object database.
- `REJECT` — user does not want the image. It is permanently excluded from ordinary future candidate pages.
- `MAYBE` — user has already reviewed the image but has not made a final decision. It is excluded from ordinary NEW-candidate pages and may appear only in an explicit MAYBE/REVISIT review.
- `UNREVIEWED` — may appear in a future candidate page.
- broken/dead/invalid candidates are permanently excluded once identified.

## Important scope rule

`KEEP` means **interesting astronomy image**, not galaxy-only. Galaxies, nebulae, clusters, supernova remnants, star-forming regions, and other scientifically/visually interesting images are all valid. Object class and observatory provenance are metadata used for routing; they are not automatic rejection criteria.

## Identity / deduplication

Future curators must deduplicate in this order where available:

1. provider + collection + archive/source ID
2. canonical source/image URL
3. SHA-256 image-content hash
4. normalized astronomical target + observatory + release ID

A card must not be rendered in the normal NEW queue when any master record already resolves to `KEEP`, `REJECT`, `MAYBE`, broken, or duplicate.

## Structure

- `gv-curation-master-*.json` — authoritative cumulative decision index.
- `sessions/` — immutable snapshots of individual curator sessions/backups.
- `selected-previews/` — lightweight visual copies of KEEP selections, organized by provenance/provider when committed.
- `audits/` — link-health, duplicate, and provenance audits.

## Observatory routing

Selection and routing are separate operations. A KEEP can later route to Hubble, Spitzer, Chandra, JWST, another observatory, or `MULTI_OBSERVATORY`. The original review decision must never be lost when routing changes.
