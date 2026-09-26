# Third-party notices

## FlightGear A350XWB exterior, flight deck, instruments, effects, sounds and related assets

- **Project:** [Ger272/A350XWB](https://github.com/Ger272/A350XWB)
- **Imported revision:** `d7e32927548d2da84ea40cc734f82d43f6ca6bc2`
- **Upstream license statement:** the upstream `README.md` says “Released under GPL2+”. The upstream `COPYING` license text is included at the repository root. The upstream material is redistributed under the terms stated in that license; review `COPYING` for the full conditions and disclaimer.
- **Credits retained from upstream `A350XWB-common.xml` and README:** Juuso Tapaninen (`jormapaappa1235`), Brendan O'Gara (`Sbyx`), Chris Leung (`ACJZA`), Chris Andrews (`DARK-L`), Joshua Davidson (`it0uchpods` / `411`), and other contributors. The source README also credits the FlightGear community and records its 2015 copyright notice.
- **Imported content:** the A350XWB-900 exterior mesh and wrapper, flight-deck mesh and wrapper, instrument submodels, textures, lights, effects, ground-service model assets, sound assets/configuration, generic FlightGear instrumentation/system XML, and cockpit camera-view configuration.

### Changes made in this repository

1. Re-targeted upstream `Aircraft/A350XWB/` references to this package's `Aircraft/A350/` installation path.
2. Removed the exterior wrapper's dynamic livery-loading code because the associated livery set/paint kit was not imported. The included base A350 texture remains assigned.
3. Removed two stray `>` characters following cockpit animation object names.
4. Integrated the community exterior and cockpit wrappers into this package's set file and common configuration.
5. Retained this repository's separate, approximate JSBSim FDM rather than importing the upstream aircraft FDM or claiming its accuracy. Local Nasal status demonstrations remain separate from upstream aircraft system logic.

The original contributors retain their upstream authorship and license rights. The changes above do not imply Airbus authorship, endorsement, technical review, certification, or validation. See the repository README for the limitations of this simulation package.
