# MultiscaleMobilityPatterns
Code for the paper "Multiscale mobility patterns and the restriction of human movement" by Dominik J Schindler, Jonathan M Clarke and Mauricio Barahona: https://arxiv.org/abs/2201.06323

## Data access

### Facebook Movement Maps

Data used in this study was accessed through Facebook's "Data for Good" program: https://dataforgood.facebook.com/dfg/tools/movement-maps. We use the raw data only in our first notebook, where we compute derivative data that can be used to reproduce all results of our study. The derivative data is available in the `data\processed\` directory.

### Geographic shape files

Shape files for the UK used in this study are obtained from the Office for National Statistics licensed under the Open Government Licence v.3.0 and contain OS data © Crown copyright and database right 2023.

- UK Local Authority Districts (LAD), May 2020: https://geoportal.statistics.gov.uk/datasets/local-authority-districts-may-2020-boundaries-uk-bgc/explore
- UK Nomenclature of Territorial Units for Statistics (NUTS), January 2018: https://geoportal.statistics.gov.uk/datasets/nuts3-jan-2018-super-generalised-clipped-boundaries-in-the-uk/explore

We also annotate maps with UK city names.

- UK Cities: https://simplemaps.com/data/gb-cities, licensed under [MIT license](https://opensource.org/license/mit/)

## Cite

Please cite our paper if you use this code in your own work:

```
@article{schindlerMultiscaleMobilityPatterns2023,
  author = {Schindler, Dominik J. and Clarke, Jonathan and Barahona, Mauricio},
  title = {Multiscale Mobility Patterns and the Restriction of Human Movement},
  publisher = {arXiv},
  year = {2023},
  doi = {10.48550/arXiv.2201.06323},
  url = {http://arxiv.org/abs/2201.06323},
}
```