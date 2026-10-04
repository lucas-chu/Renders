# Renders

Blender architectural scenes, rendered films, textures, references, source scripts, and saved animation frames.

## Projects

| Project | Scene and film location | Archive notes |
| --- | --- | --- |
| [St. Peter's Basilica](saint-peters) | [outputs](saint-peters/outputs) | Original and Beauty films, Ave Maria version, and the later ray-traced scene. The ray-traced movie was not present in the recovered files. Grass flicker and the requested more sacred atmosphere remain unresolved revisions. |
| [Colosseum](colosseum) | [original output](colosseum/output), [revised output](colosseum/v2/output) | AD 160 reconstruction, films, reference material, two saved frame sequences, and construction scripts. |
| [Château Frontenac](chateau-frontenac) | [outputs](chateau-frontenac/outputs) | Original and Beauty scenes and available film exports, soundtrack, render state and frames. Availability in this archive does not constitute a new visual-quality review. |
| [544B Presidio Boulevard](presidio-544b) | [outputs](presidio-544b/outputs) | Original and improved scenes and films, saved frames, plus earlier assets and scene-building work under `legacy/`. |

## Download

Binary assets use Git LFS. Install Git LFS before cloning to download the actual scenes, images, and videos:

```sh
git lfs install
git clone https://github.com/lucas-chu/Renders.git
```

For a small checkout, skip binary downloads initially and fetch only a project's finished outputs:

```sh
GIT_LFS_SKIP_SMUDGE=1 git clone https://github.com/lucas-chu/Renders.git
cd Renders
git lfs pull --include="saint-peters/outputs/**"
```

The archive contains approximately 17 GB of source files, including raw frames and historical versions. LFS may deduplicate identical binaries. `FILE_MANIFEST.json` records archived paths, sizes, and checksums when the upload is complete.

## Reuse and provenance

Keep each project's credits, scene notes, source references and texture licenses with its assets. Music and photographic textures have their own attribution and licensing requirements; this repository does not apply a blanket license to third-party material.

The scripts are preserved as originally used and may contain machine-specific absolute paths. Review paths before running them. Blender backups (`.blend1`) and older renders are retained to preserve the work. Python environments, package caches, unrelated app/research projects, and a dangling temporary-frame symlink are omitted.

## Import status

Archive complete: **4,912 project files**, representing **16.76 GB** of source material, across all four projects. All available saved frames are included. Every unique Git LFS object was checked for availability on GitHub.

See [FILE_MANIFEST.json](FILE_MANIFEST.json) for file sizes and content checksums, and [ARCHIVE_REPORT.json](ARCHIVE_REPORT.json) for per-project counts, remote verification, and exclusions. This verifies the upload, not the visual quality or completion of previously unfinished revisions.
