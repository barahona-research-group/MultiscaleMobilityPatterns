[![DOI](https://zenodo.org/badge/621783079.svg)](https://zenodo.org/badge/latestdoi/621783079)

# MultiscaleMobilityPatterns
Code for the paper "Multiscale mobility patterns and the restriction of human movement" by Juni Schindler, Jonathan M Clarke and Mauricio Barahona: https://arxiv.org/abs/2201.06323

## Data access

### Facebook Movement Maps

Data used in this study was accessed through Facebook's "Data for Good" program: https://dataforgood.facebook.com/dfg/tools/movement-maps. We use the raw data only in our first notebook, where we compute baseline and daily mobility networks for the UK (see paper) that can be used to reproduce all results in this study. This derivative data is available in the `data/processed/networks` directory.

### Geographic shape files

Shape files for the UK Nomenclature of Territorial Units for Statistics (NUTS), January 2018, used in this study are obtained from the Office for National Statistics licensed under the Open Government Licence v.3.0 and contain OS data © Crown copyright and database right 2023: https://geoportal.statistics.gov.uk/datasets/nuts3-jan-2018-super-generalised-clipped-boundaries-in-the-uk/explore

Shape files for the Travel to Work Areas (TTWA), December 2011, used in this study are obtained from the Office for National Statistics licensed under the Open Government Licence v.3.0 and contain OS data © Crown copyright and database right 2023: https://geoportal.statistics.gov.uk/datasets/ons::travel-to-work-areas-dec-2011-super-generalised-clipped-boundaries-in-united-kingdom-2/explore

We also annotate geographic maps with UK city names licensed under [MIT license](https://opensource.org/license/mit/): https://simplemaps.com/data/gb-cities

## Multiscale clustering

In this study, we use the ``PyGenStability`` python package for unsupervised multiscale clustering of the Facebook mobility data with Markov Stability analysis, including scale selection. Code and documentation are hosted on GitHub under a GNU General Public License: https://github.com/barahona-research-group/PyGenStability

## Cite

Please cite our paper if you use our code or data in your own work:

```
@article{schindlerMultiscaleMobilityPatterns2023,
  author = {Schindler, Juni and Clarke, Jonathan and Barahona, Mauricio},
  title = {Multiscale Mobility Patterns and the Restriction of Human Movement},
  publisher = {arXiv},
  year = {2023},
  doi = {10.48550/arXiv.2201.06323},
  url = {http://arxiv.org/abs/2201.06323},
}
```

## Licence

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.
