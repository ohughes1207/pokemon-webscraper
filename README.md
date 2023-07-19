# pokemonscraper

A custom built web scraper to collect data of all existing Pokemon and create a dataset which will be used in the creation of my Pokedex App.

### How to use

1. Install the required packages with ``pip install -r requirements.txt`` or a preferred method
2. Run the spider by executing the command ``scrapy crawl pokemonscraper -O pokemon.csv`` from the ``/PokedexApp/pokemonscraper`` directory
3. Clean and correct the data following the methods used in ``data_cleaning.ipynb``

This results in a cleaned dataset of all Pokemon as of writing and believed to be no more errors from the ones corrected in the 3rd step.
